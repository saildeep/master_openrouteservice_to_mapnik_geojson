import argparse
import requests
import json
from pyproj import transform,Proj, Transformer

parser = argparse.ArgumentParser("Openrouteservice route downloader")
parser.add_argument("-k", "--key", "--api_key", "--apikey", help="openrouteservice api key", type=str, nargs='?')
parser.add_argument("-sLat", "--start-latitude", type=float, nargs='?')
parser.add_argument("-sLng", "--start-longitude", type=float, nargs='?')
parser.add_argument("-eLat", "--end-latitude", type=float, nargs='?')
parser.add_argument("-eLng", "--end-longitude", type=float, nargs='?')
parser.add_argument("-o", "--out",type=str,nargs="?",default="out.json")

args = parser.parse_args()

endpoint = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
data = {"coordinates": [[args.start_longitude,args.start_latitude], [args.end_longitude,args.end_latitude]]}
header = {"Authorization": args.key, "Content-Type": "application/json"}
resp = requests.post(endpoint, data=json.dumps(data), headers=header)
assert resp.status_code == 200
resp_data = resp.json()
coord_list = resp_data['features'][0]['geometry']['coordinates']
projected_coord_list = []
#do this as mapnik expects to coordinates in epsg 3857 form some weird reason
wgs84 = Proj('epsg:4326')
proj = Proj('epsg:3857')
trans = Transformer.from_proj(wgs84,proj)
for lnglat in coord_list:
    a,b = trans.transform(lnglat[1],lnglat[0])

    projected_coord_list.append([a,b])

out_data = {
    "type":"FeatureCollection",
    "features":[
        {
            "type":"Feature",

            "geometry":{
                "type":"LineString",
                "coordinates":projected_coord_list
            }
         }
    ]
}
with open(args.out,'w') as f:
    json.dump(out_data,f,indent=4)


pass
