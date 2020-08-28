from time import sleep

import math
from matplotlib import colors

from main import get_route
import random
import os
import json
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


def truncate_normal(lower,upper,truncation_times_sigma=4):
    if upper < lower:
        return truncate_normal(upper,lower)

    dist = upper -lower
    mean = lower + .5 *dist
    stddev = dist/(truncation_times_sigma*2)
    randn = float('inf')
    while(randn > upper or randn < lower):
        randn = random.normalvariate(mean,stddev)
    return randn

def pick_lat_lng():
    from_lat = 48.0
    to_lat=55.0
    from_lng = 8.0
    to_lng = 13.0

    return (truncate_normal(from_lat,to_lat),truncate_normal(from_lng,to_lng))

def get_routes(num_routes = 500):
    path = "./visroutes-"+str(num_routes)+".json"
    if os.path.isfile(path):
        with open(path,'r') as f:
            return json.load(f)
    routes = []
    while len(routes) < num_routes:
        start = pick_lat_lng()
        end = pick_lat_lng()
        try:
            route = get_route(start[0],start[1],end[0],end[1],os.environ.get("API_KEY"))
            routes.append(route)


        except ConnectionError as e:
            print(e)
            sleep(5)
            continue

        print("Finished " + str(len(routes)))
        sleep(2)
    with open(path,'w') as f:
        json.dump(routes,f,indent=4)
    return routes

routes = get_routes()
normed_lengths=[]
weight_lengths=[]
route_lengths=[]
all_steps = []
all_props = []
for route in routes:
    props = route['features'][0]['properties']
    steps = list(filter(lambda x:x['type'] not in [10,11], props['segments'][0]['steps']))
    all_steps.append(steps)
    all_props.append(props)
    t = 0
    timesteps = []
    normed_length = []
    total_length = props['summary']['distance']
    total_steps = len(steps)
    for step in steps:
        t += step['distance']
        timesteps.append(t)
        normed_length.append(t / total_length)
        weight_lengths.append(1.0/total_steps)
        route_lengths.append(total_length)

    single_distances = list(map(lambda x: x['distance'], steps))
    normed_lengths = normed_lengths + normed_length


plt.hist(normed_lengths,weights=weight_lengths,bins=50)
plt.title("Density of instructions along routes")
plt.xlabel("Normalized route length")
plt.ylabel("Weighted number of turns")
plt.savefig("turn_density.pdf")
plt.clf()

x = list(map(lambda x:x['summary']['distance']/1000,all_props))
y = list(map(lambda x:len(x),all_steps))
plt.scatter(x,y,marker=".")
plt.xlabel("Route length in km")
plt.ylabel("Number of turns")
plt.savefig("turn_scatter.pdf")
print("scatter pearsonr", pearsonr(x,y))
plt.clf()



plt.hist(list(map(lambda x:x['summary']['distance']/1000,all_props)),bins=10)
plt.xlabel("Route length in km")
plt.ylabel("Number of routes")
plt.savefig("route_length.pdf")
plt.clf()

bins = {}
for l, rl,wl in zip(normed_lengths,route_lengths,weight_lengths):
    index = math.floor(rl/(100 * 1000) )
    collection =  bins.get(index,[])
    collection.append(l)
    bins[index] = collection
keys = sorted(list(bins.keys()))
values = list(map(lambda x:bins[x],keys))
labels = list(map(lambda x:"{0}km-{1}km".format(x*100,(x+1)*100), range(8)))

plt.hist(values,bins=25,histtype="bar",label=labels,density=True)
plt.legend()
plt.savefig('categorized_route_length.pdf')
plt.clf()


x = list(map(lambda x:x['summary']['distance']/1000,all_props))
y = list(map(lambda x:len(x),all_steps))
plt.hist2d(x,y,bins=13)
plt.xlabel("Route length in km")
plt.ylabel("Number of turns")
cb = plt.colorbar()
cb.set_label("Number of routes")
plt.savefig("turn_heatmap.pdf")
plt.clf()

print(len(all_steps))