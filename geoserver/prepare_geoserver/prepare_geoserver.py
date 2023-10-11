import requests
import json

class GeoserverRest:

    def __init__(self, base_url, data_dir):
        self.base_url = base_url
        self.data_dir = data_dir
        self.username = 'admin'
        self.password = 'geoserver'
    
    def get_json_response(self, sub_path) -> str:
        url = f'{self.base_url}/{sub_path}.json'
        response = requests.get(url, auth=(self.username, self.password))
        if response.ok:
            return response.json()
        else:
            return "Not a valid response"

    def post_json(self, sub_path, data) -> dict:
        headers = {'content-type': 'application/json'}
        url = f'{self.base_url}/{sub_path}'
        response = requests.post(url,
                                    data=data,
                                    headers=headers,
                                    auth=(self.username, self.password))
        return {"status_code": response.status_code, "Error": response.text}

    def get_geoserver_version(self):
        json = self.get_json_response('about/version')
        return json['about']['resource'][0]

    def get_layers(self):
        json = self.get_json_response('layers')
        return json

    def add_workspace(self, name):
        headers = {'content-type':'application/json'}
        data = json.dumps({
                        "workspace": {
                            "name": name
                        }
                    })
        response = requests.post(f'{self.base_url}/workspaces', data=data, headers=headers, auth=(self.username, self.password))
        return response.ok

    def remove_workspace(self, name):
        response = requests.delete(f"{self.base_url}/workspaces/{name}?recurse=true", auth=(self.username, self.password))
        return response.ok


    def add_shapefile_store(self, workspace, store_name):
        data = f"{self.data_dir}/cbs/CBS_gemeenten2022.shp"
        response = requests.put(f'{self.base_url}/workspaces/{workspace}/datastores/{store_name}/external.shp',
                                data=data,
                                auth=(self.username, self.password))
        return response.ok

    def add_geopackage_store(self, workspace, store_name):
        data = f'{self.data_dir}/cbs/WijkBuurtkaart_2022_v0.gpkg'
        response = requests.put(f'{self.base_url}/workspaces/{workspace}/datastores/{store_name}/external.gpkg', 
                                data=data,
                                auth=(self.username, self.password))
        return response.ok

    def add_style(self, file):
        location = f'own/{file}'
        data = json.dumps({
                "style": {
                    "name": file.split('.')[0],
                    "filename": location
                }
            })
        result = self.post_json("styles", data)
        print(result)

    def get_layer(self, workspace, store, layer):
        return self.get_json_response(f"workspaces/{workspace}/datastores/{store}/featuretypes/{layer}")

    def set_layer(self, workspace, store, data):
        return self.post_json(f"workspaces/{workspace}/datastores/{store}/featuretypes", data)
        
if __name__ == '__main__':
    data_dir = '/opt/geoserver_data/data'
    base_url = 'http://localhost:8080/geoserver/rest'
    rest = GeoserverRest(base_url, data_dir)
    workspace = 'test'
    store = 'nyc'
    data = rest.get_layer(workspace,store,'Subway')
    data['featureType']['name'] = 'Subway2'
    data['featureType']['nativeName'] = 'Subway2'
    data['featureType']['title'] = 'Subway2'
    print(rest.set_layer(workspace, store, json.dumps(data)))
    # print(rest.get_geoserver_version())
    # print(rest.get_layers())
    # print(rest.add_workspace('test'))
    # print(rest.remove_workspace('test'))
    # print(rest.add_shapefile_store('test','CBS_gemeenten2022'))
    # print(rest.add_geopackage_store('test','WijkBuurtkaart_2022_v0'))

    # print(rest.add_style('gemeente_water.sld'))


