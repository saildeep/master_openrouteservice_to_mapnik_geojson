import argparse
import requests
import json

parser = argparse.ArgumentParser("Openrouteservice route downloader")
parser.add_argument("-k", "--key", "--api_key", "--apikey", help="openrouteservice api key", type=str, nargs='?')
parser.add_argument("-sLat", "--start-latitude", type=float, nargs='?')
parser.add_argument("-sLng", "--start-longitude", type=float, nargs='?')
parser.add_argument("-eLat", "--end-latitude", type=float, nargs='?')
parser.add_argument("-eLng", "--end-longitude", type=float, nargs='?')

args = parser.parse_args()

endpoint = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
data = {"coordinates": [[args.start_longitude,args.start_latitude], [args.end_longitude,args.end_latitude]]}
header = {"Authorization": args.key, "Content-Type": "application/json"}
resp = requests.post(endpoint, data=json.dumps(data), headers=header)
assert resp.status_code == 200
resp_data = resp.json()
pass
