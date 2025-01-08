from main.pluginSystem import dataProviderCore
from main.pluginSystem.plugin_register import *
from main.utils import decrypt_parameter
from main.models import *
import requests

class ElabFTW(dataProviderCore):

    def connection(self,request,host_p):
        ELNobj = DataProvider.objects.get(name="ElabFTW")
        settings =  ProviderUserSetting.objects.get(provider=ELNobj, user = request.user , host=host_p)
        apiKey = decrypt_parameter((settings.API_key).encode())
        return apiKey


    def getMetadata(self,request, elements):
        apiKey = self.connection(request, self.host)
        metadata = []
        for el in elements:
            try:
                response = requests.get(self.host + "/api/v2/experiments" + f"/{el.id_inside_Data_Provider}",
                                        headers={"Content-Type": "application/json", "Authorization": apiKey},
                                        verify=False)
                experimentsData = response.json()

                info = {"Type": el.type,
                        "Name": el.name,
                        "Created_at": experimentsData["created_at"],
                        "ID": experimentsData["id"],
                        "Host": self.host,
                        "Body_html": experimentsData["body_html"],

                        }

                metadata.append(info )


            except Exception as e:
                #print(request, 'Error connecting to elabFTW: {}'.format(str(e)))
                msg = 'Error connecting to elabFTW: {}'.format(str(e))
                #print(msg)

        return metadata

    def getElements(self,request):

        apiKey = self.connection(request, self.host)
        experiments = []
        try:
            response = requests.get(self.host + "/api/v2/experiments",
                                    headers={"Content-Type": "application/json", "Authorization": apiKey}, verify=False)
            experimentsData = response.json()
            ids = 0
            for e in experimentsData:
                experiments.append({"id": ids, "origin_id": str(e["id"]), "title": e["title"], "types": "Experiment"}, )
                ids += 1;
            return experiments
        except Exception as e:
            #print(request, 'Error connecting to elabFTW: {}'.format(str(e)))
            msg = 'Error connecting to elabFTW: {}'.format(str(e))
            #print(msg)
            return experiments





def initialize() -> None:
    register("ElabFTW", ElabFTW)