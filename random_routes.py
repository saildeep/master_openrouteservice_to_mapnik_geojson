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


for i in range(10):
    start = pick_lat_lng()
    end = pick_lat_lng()
    try:
        route = get_route(start[0],start[1],end[0],end[1],os.environ.get("API_KEY"))
        props =  route['features'][0]['properties']
        steps =props['segments'][0]['steps']
        t =0
        timesteps = []

        for step in steps:
            timesteps.append(t)
            t+=step['distance']
        plt.plot(timesteps)

    except AssertionError as e:
        print(e)
        continue
    sleep(1)
plt.show()