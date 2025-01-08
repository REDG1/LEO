from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from main.pluginSystem import plugin_loader, plugin_register
from django.http import HttpResponse, HttpResponseRedirect
from main.models import *
from django.urls import reverse
import datetime
import requests
import json
import sys

from django.http import JsonResponse
import mysql.connector

from main.utils import encrypt_parameter, decrypt_parameter

from omero.gateway import BlitzGateway


from main.omero_metadata.populate import ParsingContext
from main.omero_metadata.populate import parse_target_object
from omero import client





if not any(elem in sys.argv for elem in ('makemigrations', 'migrate')):

    data_plugins = DataProvider.objects.all()
    # load the plugins
    print("Loading plugins ...")
    plugins = [dp.name for dp in data_plugins ]
    plugin_loader.load_plugins(plugins)
    plugins_names = plugin_register.getDPNames()
    print("plugins added")





def populateTable(request):
    result = {"populated": "False"}
    if request.method == "POST":
        O_user = request.session.get('O_user')
        O_pwd = request.session.get('O_pwd')
        O_host = request.session.get('O_host')

        port = 4064  # SSL

        O_client = client(O_host, port)
        O_client.setAgent("OMERO.populate_metadata")
        O_client.enableKeepAlive(60)
        context_class = ParsingContext



        try:
            dataTable = json.loads(request.body)["table"]
            dataID = json.loads(request.body)["ID"]
            type = json.loads(request.body)["Type"]

            targetDataset = parse_target_object(str(type)+":" + str(dataID))
            print(targetDataset)

            O_client.createSession(O_user, decrypt_parameter(O_pwd.encode()))

            con = BlitzGateway(client_obj=O_client)
            print((str(type)).lower())
            Prevannotations = con.getObjects("Annotation", opts={(str(type)).lower(): int(dataID)})
            inputHeadears = []
            for ih in dataTable["headers"]:
                inputHeadears.append(ih["value"])
            for a in Prevannotations:
                if str(a.OMERO_TYPE) == "<class 'omero.model.FileAnnotationI'>":
                    orig_table_file = con.getObject("OriginalFile", a.file.id)


                    if orig_table_file.mimetype == "OMERO.tables":
                        resources = con.c.sf.sharedResources()
                        Ptable = resources.openTable(orig_table_file._obj)
                        headers = Ptable.getHeaders()
                        print("#"*30)
                        #print(list(filter(lambda x: x[0] != '_' and callable(getattr(orig_table_file, x)), dir(orig_table_file))))
                        #print(a.getId(), a.OMERO_TYPE)
                        #print(a.getParent())
                        #print(orig_table_file.getParent())
                        otype= None
                        oid= None
                        for ptype in ["project", "dataset", "image"]:
                            links = list(a.getParentLinks(ptype))
                            if len(links) > 0:
                                obj_link = links[0].parent
                                otype = ptype
                                oid = obj_link.id.val
                                break

                        print("columns")
                        rowCount = Ptable.getNumberOfRows()
                        data = Ptable.readCoordinates(range(rowCount))
                        for col in data.columns:
                            print("Data for Column: ", col.name)
                            for v in col.values:
                                print("   ", v)


                        print("#"*30)
                        arrayHeaders = []
                        for h in headers:
                            if h.name != "Image":
                                arrayHeaders.append(h.name)

                        are_equal = set(arrayHeaders) == set(inputHeadears)
                        origTypeID = (str(type)).lower()+":"+str(dataID)
                        prevTypeID = ""
                        if oid and otype:
                            prevTypeID = otype+":"+str(oid)

                        #print("Types, IDs", origTypeID, " - ", prevTypeID)



                        if are_equal and (origTypeID==prevTypeID):
                            print(a.file.id)
                            con.deleteObjects('OriginalFile', [str(a.file.id._val)], wait=True)
                        #print(are_equal)
                        Ptable.close()



            ctx = context_class(
                O_client,
                targetDataset,
                dictionary_data=dataTable,
                column_types=None)

            ctx.parse_dictionary()

            result = {"populated": "True"}
        except Exception as e:
            print(e)
            return JsonResponse({"msg": str(e), "populated": False}, status=400)
        finally:
            pass
        O_client.closeSession()

    return JsonResponse(result)



def removeLinks(request):
    result = {"deleted": "False"}
    if request.method == "POST":
        try:
            data = json.loads(request.body)["data"]
            #print(data)
            linkObject = Link.objects.get(pk=int(data))
            linkObject.delete()
            result =  {"deleted": "True"}
        except Exception as e:
            print(e)
            return JsonResponse({"msg": str(e), "deleted": False}, status=400)

    return JsonResponse(result)

def removeSettings(request):
    result = {"deleted": "False"}
    if request.method == "POST":

        try:
            data = json.loads(request.body)["data"]
            #print(data)
            settingObject = ProviderUserSetting.objects.get(pk=int(data))
            settingObject.delete()
            result =  {"deleted": "True"}
        except Exception as e:
            print(e)
            return JsonResponse({"msg": str(e), "deleted": False}, status=400)

    return JsonResponse(result)

def saveSettings(request):
    if request.method == "POST":

        try:
            data = json.loads(request.body)["data"]
            #print(data)
            provider = DataProvider.objects.get(name=data["provider"])
            if data["id"].startswith("t-"):
                newRegister = ProviderUserSetting(
                    host=data["host"],
                    API_key=encrypt_parameter(data["API_Key"]).decode(),
                    provider=provider,
                    user=request.user
                )
                newRegister.save()  # Save the new instance
            else:
                newRegister = ProviderUserSetting.objects.get(pk=data["id"])
                newRegister.host = data["host"]
                newRegister.API_key = encrypt_parameter(data["API_Key"]).decode()
                newRegister.provider = provider
                newRegister.save()  # Save the updated instance

            saveReg = {
                "id": str(newRegister.pk),
                "host": newRegister.host,
                "API_Key":  decrypt_parameter((newRegister.API_key).encode()) ,
                "provider": newRegister.provider.name
            }

            return JsonResponse({"msg": "success", "saveReg": saveReg})
        except Exception as e:
            print(e)
            return JsonResponse({"msg": str(e)}, status=400)

    dataout = {"msg": ""}
    return JsonResponse(dataout)

@login_required()
def settings(request):
    providerSet = ProviderUserSetting.objects.filter(user=request.user)
    providers = [ dp.name for dp in  DataProvider.objects.all()  if dp.name != "OMERO" ]
    arrayPS =  [{"id":str(ps.pk), "host":ps.host, "API_Key":decrypt_parameter((ps.API_key).encode()), "provider": ps.provider.name} for ps in providerSet ]
    context = {"providerSet":arrayPS,
               "providers":providers,
               "user": str(request.user)}
    return render(request, 'settings.html', context)


def login(request):
    #print("entra a login")
    #print( request.user.is_authenticated )
    if request.POST:
        #print(request.POST)
        if request.method == 'POST':

            username = request.POST.get('user')
            host = request.POST.get('host')
            password = request.POST.get('pswd')
            #print(username," - ",host," - ", password)


            # Authenticate user against OMERO
            try:

                # If authentication is successful, log the user into Django
                user = authenticate(request, username=username, password=password, host=host)

                if user is not None:
                    #print('valid user', user)
                    if user.is_active:
                        #auth_login(request, user, backend='main.customAuth.OMEROBackend')
                        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        if user.is_authenticated:
                            request.session['O_user'] = username
                            request.session['O_pwd'] = encrypt_parameter(password).decode()
                            #request.session['O_pwd'] = "test"
                            request.session['O_host'] = host
                            #print('authenticated')

                            Provider = DataProvider.objects.get(name="OMERO")
                            usersettings = ProviderUserSetting.objects.filter(user= request.user, provider=Provider, host=host )
                            if not usersettings:

                                newRegister = ProviderUserSetting(
                                    host=host,
                                    API_key= encrypt_parameter("").decode(),
                                    provider=Provider,
                                    user=request.user
                                )
                                newRegister.save()
                                return redirect('home:settings')
                            else:
                                return redirect('home:home')  # Redirect to dashboard upon successful login
                        else:
                            print("error in authentification")
                            messages.error(request, "error in authentification")
                            return render(request, 'login.html')

                else:
                    print('Invalid username or password.')
                    messages.error(request, 'Invalid username or password.')
                    return render(request, 'login.html')


            except Exception as e:
                messages.error(request, 'Error connecting to OMERO: {}'.format(str(e)))
                print('Error connecting to OMERO: {}'.format(str(e)))
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@login_required()
def linking(request):

    #Get elements from OMERO
    dataProviders = []

    # plugin_omero = plugin_register.create("OMERO", request.session['O_host'])
    # getOmeroElements = plugin_omero.getElements(request)
    # omeroDict = {"title": "OMERO", "host": request.session['O_host'], "element": getOmeroElements}
    # dataProviders.append(omeroDict)
    # del plugin_omero
    # get elements from other plugins
    setProvs =  ProviderUserSetting.objects.filter(user=request.user)
    for st in setProvs:
        plugin_obj = plugin_register.create(st.provider.name,st.host)
        getObjElements = plugin_obj.getElements(request)
        objDict = {"title": st.provider.name,  "host": st.host, "element": getObjElements}
        dataProviders.append(objDict)


    #print("DataProviders: ", dataProviders )
    context = {"dataProviders": dataProviders   }

    return render(request, 'linking.html', context)

def evalparentLevel(obj, level):
    level += 1
    if obj.parent is not None:
        level = evalparentLevel(obj.parent, level)
    return level

def createLinkDictionaries(links):
    try:
        providers = ProviderUserSetting.objects.all()
    except Exception as e:
        raise RuntimeError("Error fetching data providers: " + str(e))
    res= {"Links": []}
    for link in links:
        linkDict = {"id": link.id, "data": []}
        #print("%" * 30,"Link ID:" ,link.id)
        for provider in providers:
            #print("#" * 30, provider.provider.name)

            elementsOfcurrentProvider = link.Element2link.filter(provider = provider)
            if len(elementsOfcurrentProvider) > 0:
                provDict = {"id": provider.id, "title": provider.provider.name, "children": []}
                #print("elements:", elementsOfcurrentProvider)
                levelPerElement = [evalparentLevel(e,0) for e in elementsOfcurrentProvider ]
                #print("levels", levelPerElement)
                tempEl = []
                for l in range(max(levelPerElement) ,0,-1):
                    #print("level:", l)
                    indices  = [i for i in range(len(levelPerElement)) if levelPerElement[i] == l]
                    for i in indices:
                        tempChildren = tempEl

                        elementDict = {
                            "id": elementsOfcurrentProvider[i].id,
                            "title": elementsOfcurrentProvider[i].name,
                            "children": [],
                            "elemnt_type": elementsOfcurrentProvider[i].type,
                            "provider": elementsOfcurrentProvider[i].provider.id,
                            "parent": elementsOfcurrentProvider[i].parent.id if elementsOfcurrentProvider[i].parent is not None else "False",
                            "originId": elementsOfcurrentProvider[i].id_inside_Data_Provider

                        }

                        if l == max(levelPerElement) and l != 1:
                            tempChildren.append(elementDict)
                        elif l == max(levelPerElement) and l == 1:
                            tempEl.append(elementDict)
                        else:
                            tempEl=[]

                            for ch in tempChildren:
                                if elementsOfcurrentProvider[i].id == ch["parent"]:
                                    elementDict["children"].append(ch)
                                else:
                                    tempEl.append(ch)
                            tempEl.append(elementDict)

                    #print(f"element in level{l}:", tempEl)
                provDict["children"]=tempEl

                linkDict["data"].append(provDict)
        res["Links"].append(linkDict)
    #print(res)
    return res

@login_required()
def currentLink(request):
    user = request.user
    links = Link.objects.filter(user=user)
    context = {"Links":[]}
    #print(links)
    #try:
    newDict = createLinkDictionaries(links)
    context = newDict
    #except Exception as e:
    #    print(e)
    return render(request, "current_links.html", context)


@login_required()
def logout_view(request):
    logout(request)
    return redirect('home:login')

@login_required()
def home(request):
    #print(request.user)
    return render(request, 'home.html')



def saveElements(provider,host,elements, array, parentObj, user):


    elProvider = ProviderUserSetting.objects.get(provider__name=provider, host=host, user=user)

    elName = elements["title"]
    elType = elements["types"]
    #elID = elements["id"]
    elID = elements["origin_id"]

    try:
        elID = int(elID)
    except ValueError:
        elID =-1

    try:
        elements["parent"]
        if elements["parent"] != "false":
            #print("parentOBJ: ",parentObj)
            elParent = Element.objects.get(id = parentObj.id)
            newElement = Element(name=elName, provider=elProvider, type=elType, id_inside_Data_Provider=elID, parent=elParent)
        else:
            newElement = Element(name=elName, provider=elProvider, type=elType, id_inside_Data_Provider=elID)
    except:
        newElement = Element(name=elName, provider=elProvider, type=elType,id_inside_Data_Provider=elID )

    #check if the new element exist

    prevElements = Element.objects.filter(provider=elProvider, id_inside_Data_Provider=elID,type=elType, name=elName )
    if not prevElements:
        newElement.save()
        array.append(newElement)
    else:
        array.append(prevElements[0])
    #recursive function for childrens

    try:
        elements["children"]
        if len(elements["children"]) != 0:
            parent = array[-1]
            for children in elements["children"]:
                array = saveElements(provider,host ,children, array, parent,user)
    except:
        pass

    return array


def saveLinks(ObjArray, user):
    existing_links = Link.objects.filter(user=user)
    element_ids = {element.id for element in ObjArray}
    #check if the link exist

    existflag =  False
    for link in existing_links:
        # check if the link exist
        if element_ids == set(link.Element2link.values_list('id', flat=True)):
            print(f"Link already exists for user {user} with elements {element_ids}")
            existflag = True
            break
    if existflag == False:
        link = Link(user=user)
        link.save()
        for obj in ObjArray:
            link.Element2link.add(obj)


def saveElementsAndLinks(request):
    datain ={}

    if request.method == "POST":
        try:
            data = json.loads(request.body)["data"]
            #print(data)
            elements2link = []
            for dGroups in data:
                for children in dGroups["children"]:
                    #print("Group: ", dGroups["provider"], dGroups["host"] , " Children: ", children  )
                    elements2link = saveElements(dGroups["provider"], dGroups["host"] ,children, elements2link, None, request.user)
            #print(elements2link)
            saveLinks(elements2link,request.user)
            datain = data
        except Exception as e:
            return JsonResponse({"msg": e}, status=400)
    dataout = {"msg":""}
    return JsonResponse(dataout)

def getMetadata(request):
    #print(request)
    dataout = {"metadata":[]}
    if request.method == "GET":
        idLInks = request.GET.get('idlink')
        #user = request.user
        link = Link.objects.get(id=int(idLInks))

        ProvSettings = ProviderUserSetting.objects.filter(user=request.user)

        for ps in ProvSettings:
            provider = DataProvider.objects.get(name=ps.provider.name)
            plugin_obj = plugin_register.create(provider.name, ps.host)
            elOfcurrentProvider = link.Element2link.filter(provider=ps)
            #print("$" * 30, "Provider: ", provider)
            if len(elOfcurrentProvider) > 0:
                #print(elOfcurrentProvider)
                data = plugin_obj.getMetadata(request, [ep for ep in elOfcurrentProvider])
                ProviderInfo = {"provider":provider.name, "data": data }

                dataout["metadata"].append(ProviderInfo)


    return JsonResponse(dataout)
