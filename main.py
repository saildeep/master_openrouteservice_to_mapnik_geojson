import argparse
import requests
import json
from pyproj import transform,Proj, Transformer



def get_route(sLat,sLng,eLat,eLng,key,toproj='epsg:4326'):
    endpoint = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    data = {"coordinates": [[sLng,sLat], [eLng,eLat]]}
    header = {"Authorization":key, "Content-Type": "application/json"}
    resp = requests.post(endpoint, data=json.dumps(data), headers=header)
    if resp.status_code != 200:
        raise ConnectionError(resp.status_code)
    resp_data = resp.json()
    coord_list = resp_data['features'][0]['geometry']['coordinates']
    projected_coord_list = []
    #do this as mapnik expects to coordinates in epsg 3857 form some weird reason
    wgs84 = Proj('epsg:4326')
    proj = Proj(toproj)
    trans = Transformer.from_proj(wgs84,proj)
    for lnglat in coord_list:
        a,b = trans.transform(lnglat[1],lnglat[0])

        projected_coord_list.append([a,b])

    additional_data = resp_data['features'][0]['properties']
    out_data = {
        "type":"FeatureCollection",
        "features":[
            {
                "type":"Feature",

                "geometry":{
                    "type":"LineString",
                    "coordinates":projected_coord_list
                },
                "properties":additional_data,

             }
        ]
    }
    return out_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Openrouteservice route downloader")
    parser.add_argument("-k", "--key", "--api_key", "--apikey", help="openrouteservice api key", type=str, nargs='?')
    parser.add_argument("-sLat", "--start-latitude", type=float, nargs='?')
    parser.add_argument("-sLng", "--start-longitude", type=float, nargs='?')
    parser.add_argument("-eLat", "--end-latitude", type=float, nargs='?')
    parser.add_argument("-eLng", "--end-longitude", type=float, nargs='?')
    parser.add_argument("-o", "--out", type=str, nargs="?", default="out.json")

    args = parser.parse_args()

    out_data = get_route(args.start_latitude,args.start_longitude,args.end_latitude,args.end_longitude,args.key,toproj='epsg:3857')
    with open(args.out, 'w') as f:
        json.dump(out_data, f, indent=4)

pass
