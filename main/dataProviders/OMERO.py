from main.pluginSystem import dataProviderCore
from main.pluginSystem.plugin_register import *
from omero.gateway import BlitzGateway
from main.utils import decrypt_parameter
import copy


class omero(dataProviderCore):
    ### Data provider name, this name must be the same in the register() function
    name = "OMERO"

    def connection(self, request):
        try:
            O_user = request.session.get('O_user')
            O_pwd = request.session.get('O_pwd')
            O_host = request.session.get('O_host')

            con = BlitzGateway(O_user, decrypt_parameter(O_pwd.encode()), host=O_host, secure=True)
            con.connect()

            ### Test conection ###
            #print("Member of:")
            for g in con.getGroupsMemberOf():
                print("   ID:", g.getName(), " Name:", g.getId())
            group = con.getGroupFromContext()
            print("Current group: ", group.getName())
            msg = 'Successful connection to OMERO'
            ######
            return msg, con
        except Exception as e:
            #print(request, 'Error connecting to OMERO: {}'.format(str(e)))
            msg = 'Error connecting to OMERO: {}'.format(str(e))
            return msg, None

    def getMetadata(self, request, elements):
        msg, con = self.connection(request)
        metadata = []
        if con:

            #extract child elements
            childs = []
            parents = []



            for el in elements:
                evalParent =  [p for p in elements if p.parent == el]
                if len(evalParent) == 0:
                    childs.append(el)
                else:
                    parents.append(el)

            #print([(p.name,p.type) for p in parents])

            for p in parents:
                obj = con.getObject(p.type, p.id_inside_Data_Provider)
                if obj:

                    info = {"Type": p.type,
                            "Name": p.name,
                            "Owner": obj.getOwnerOmeName(),
                            "ID": p.id_inside_Data_Provider,
                            "Annotations": {},
                            }



                    # print(info["Annotations"])
                    annotations = []
                    [annotations.append(ann1) for ann1 in obj.listAnnotations()]

                    info["Annotations"] = self.getfileAnnotations(annotations, con, p.id_inside_Data_Provider,
                                                                  objType=str(p.type).lower(), ann=info["Annotations"])



                else:
                    info = {"Type": p.type,
                            "Name": p.name,
                            "Owner": "Orphaned",
                            "ID": p.id_inside_Data_Provider,
                            "Annotations": {},
                            }



                metadata.append(info)



            for ch in childs:

                obj = con.getObject(ch.type, ch.id_inside_Data_Provider)
                #extract metadata acording type
                if ch.type == "Dataset":
                    info = {"Type": ch.type,
                            "Name": ch.name,
                         "Owner": obj.getOwnerOmeName(),
                         "ID": obj.getId(),
                         "Project": obj.getParent().getName(),
                     }
                    """"""
                elif ch.type == "Image":
                    image_name = obj.getName()
                    image_id = obj.getId()
                    datPa = obj.getParent()
                    if datPa:
                        datSetPar = datPa.getName()
                        datSetParID = datPa.getId()
                        if datPa.getParent():
                            datProPar = datPa.getParent().getName()
                            datProID = datPa.getParent().getId()

                        else:
                            datProPar = "Orphan"
                            datProID = "Orphan"

                    else:
                        datSetPar = "Orphan"
                        datProPar = "Orphan"
                        datProID = "Orphan"
                        datSetParID = "Orphan"

                    info = {"Type": ch.type,
                            "ID": image_id,
                             "Name": image_name,
                             "Dataset": datSetPar,
                             "DatasetID": datSetParID,
                             "Project": datProPar,
                             "ProjectID": datProID,
                             "Annotations": {},
                             #"Parent_File_Annotations": {},
                             }

                    #get all list annotations
                    annotations = obj.listAnnotations()



                    # get Map annotations
                    info["Annotations"]= self.getMapAnnotations(annotations, ann={})


                    # get File annotations
                    annotations = con.getObjects("Annotation", opts={'image': image_id})


                    info["Annotations"]= self.getfileAnnotations( annotations, con, image_id,objType="image" ,ann = info["Annotations"])



                    #annotations = con.getObjects("Annotation", opts={'dataset': datSetParID})
                    #info["Parent_File_Annotations"] = self.getfileAnnotations( annotations, con, datSetParID ,info["Parent_File_Annotations"])

                    #annotations = con.getObjects("Annotation", opts={'project': datProID})
                    #info["Parent_File_Annotations"] = self.getfileAnnotations( annotations, con, datProID ,info["Parent_File_Annotations"])

                else:
                    info = {"Type":ch.type,
                            "Name": ch.name,
                            "owner": obj.getOwnerOmeName(),
                            "id": obj.getId()
                    }
                metadata.append(info)

        #print("METADATA OMERO: ", metadata)
        if con:
            con.close()

        return metadata

    def getMapAnnotations(self, annotations, ann={}):

        for a in annotations:
            if str(a.OMERO_TYPE) == "<class 'omero.model.MapAnnotationI'>":
                mapv = {"Type": "Map Annotation"}
                for indx, mvals in enumerate(a.mapValue):
                    mapv["map" + str(indx)] = ["Key: " + mvals.name, " Value: " + mvals.value]
                ann.setdefault("Annotation" + str(a.id), mapv)
        return ann


    def getfileAnnotations(self, annotations,con, ObjId, objType="image", ann={}):
        for a in annotations:

            if str(a.OMERO_TYPE) == "<class 'omero.model.FileAnnotationI'>":

                orig_table_file = con.getObject("OriginalFile", a.file.id)

                if orig_table_file.mimetype == "OMERO.tables":
                    mapv = {"Type": "File Annotation"}
                    resources = con.c.sf.sharedResources()
                    table = resources.openTable(orig_table_file._obj)

                    # Find the column index for the column containing image names
                    image_name_col_index = -1
                    populateID = False
                    headers = table.getHeaders()
                    rowCount = table.getNumberOfRows()


                    if objType == "image":
                        #print("|"*50)
                        #print(ObjId)

                        for i, col in enumerate(headers):
                            if col.name == "Image":
                                image_name_col_index = i
                                break
                            if col.name == "Image ID":
                                # if col.name == "Image":
                                image_name_col_index = i
                                populateID = True
                                break



                        if image_name_col_index != -1:
                            # Iterate over rows and find the row corresponding to the image ID

                            data0 = table.read([image_name_col_index], 0, rowCount)
                            for row_index, row in enumerate(data0.columns):
                                dataV = row.values
                                #print(dataV)
                                #print(ObjId in dataV)

                                if ObjId in dataV:
                                    if populateID == False:

                                        index = dataV.index(ObjId)

                                        data = table.read([x for x in range(len(headers))], index, index + 1)
                                        for col in data.columns:
                                            mapv[f"{col.name}"] = col.values[0]

                                    else:
                                        index = dataV.index(ObjId)
                                        data = table.read([x for x in range(len(headers))], index, index + 1)
                                        for col in data.columns:
                                            mapv[f"{col.name}"] = col.values[0]
                    else:


                        data = table.read(range(len(headers)), 0,rowCount)
                        for col in data.columns:
                            #print("vals", [vals for vals in col.values])
                            mapv[f"{col.name}"] = [vals for vals in col.values]


                    table.close()
                    #print(mapv)
                    #print("|" * 50)
                    if len(mapv) > 1:

                        ann.setdefault("Annotation" + str(a.id), mapv)
        return ann




    def getElements(self, request):
        msg, con = self.connection(request)
        pData = []
        if con is not None:
            #my_exp_id = con.getUser().getId()
            #all_projects = con.getObjects("Project", opts={"owner": my_exp_id})
            all_projects = con.getObjects("Project", opts={})
            #orp_datasets = con.getObjects("Dataset", opts={'orphaned': True, "owner": my_exp_id})
            orp_datasets = con.getObjects("Dataset", opts={'orphaned': True})
            orp_datasets = list(orp_datasets)

            pData = []
            ids = 0
            if len([od for od in orp_datasets]) > 0:
                pInfoOrphan = {"id": ids, "origin_id": "p-orphan", "title": "Orphaned datasets", "children": [],
                               "parent": "false",
                               "types": "Project"}

                parentID0 = ids
                ids += 1;

                for dataset in orp_datasets:

                    dInfo = {"id": ids, "origin_id": str(dataset.getId()), "title": dataset.getName(), "types": "Dataset",
                             "children": [], "parent": parentID0}
                    pInfoOrphan["children"].append(dInfo)

                    parentID1 = ids
                    ids += 1;

                    for image in dataset.listChildren():
                        iInfo = {"id": ids, "origin_id": str(image.getId()), "title": image.getName(), "types": "Image",
                                 "parent": parentID1}
                        dInfo["children"].append(iInfo)

                        ids += 1;
                pData.append(pInfoOrphan)

            for project in all_projects:
                pInfo = {"id": ids, "origin_id": str(project.getId()), "title": project.getName(), "parent": "false",
                         "types": "Project", "children": []}
                parentID0 = ids
                ids += 1;
                for dataset in project.listChildren():
                    dInfo = {"id": ids, "origin_id": str(dataset.getId()), "title": dataset.getName(),
                             "types": "Dataset",
                             "parent": parentID0, "children": []}
                    pInfo["children"].append(dInfo)
                    parentID1 = ids
                    ids += 1;

                    for image in dataset.listChildren():
                        iInfo = {"id": ids, "origin_id": str(image.getId()), "title": image.getName(), "types": "Image",
                                 "parent": parentID1}
                        dInfo["children"].append(iInfo)
                        ids += 1;
                pData.append(pInfo)

        #print(msg, " pData: ", pData)
        if con:
            con.close()

        return pData

def initialize() -> None:
    register("OMERO", omero)

