from time import sleep

from main import get_route
import random
import os
import matplotlib.pyplot as plt

def pick_lat_lng():
    from_lat = 47.0
    to_lat=53.0
    from_lng = 9
    to_lng = 11
    return (random.uniform(from_lat,to_lat),random.uniform(from_lng,to_lng))


normed_lengths = []
for i in range(100):
    start = pick_lat_lng()
    end = pick_lat_lng()
    try:
        route = get_route(start[0],start[1],end[0],end[1],os.environ.get("API_KEY"))
        props =  route['features'][0]['properties']
        steps =props['segments'][0]['steps']
        t =0
        timesteps = []
        normed_length = []
        total_length = props['summary']['distance']
        for step in steps:
            timesteps.append(t)
            normed_length.append(t/total_length)
            t+=step['distance']
        single_distances = list(map(lambda x:x['distance'],steps))
        normed_lengths.append(normed_length)

    except ConnectionError as e:
        print(e)
        continue
    sleep(2)
plt.hist(normed_lengths,bins=10)
plt.show()