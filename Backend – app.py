from flask import Flask, jsonify
import networkx as nx
import random
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

nodes = ["Tehran","Mashhad","Isfahan","Tabriz","Shiraz","Ahvaz","Qom","Kermanshah","Urmia",
         "Zahedan","Rasht","Yazd","Arak","Kerman","Bandar Abbas","Hamedan","Sanandaj",
         "Khorramabad","Birjand","Sari","Bojnurd","Gorgan","Zanjan","Qazvin","Kashan",
         "Ardabil","Babol","Shahrekord","Dezful","Khoy","Bushehr"]

population = { "Tehran":13,"Mashhad":3.5,"Isfahan":2,"Tabriz":1.7,"Shiraz":1.6,"Ahvaz":1.4,"Qom":1.3,
"Kermanshah":1.2,"Urmia":1.1,"Zahedan":0.9,"Rasht":1.0,"Yazd":0.8,"Arak":0.9,"Kerman":0.9,
"Bandar Abbas":0.7,"Hamedan":0.9,"Sanandaj":0.7,"Khorramabad":0.5,"Birjand":0.3,"Sari":0.5,
"Bojnurd":0.3,"Gorgan":0.4,"Zanjan":0.4,"Qazvin":0.5,"Kashan":0.3,"Ardabil":0.5,"Babol":0.4,
"Shahrekord":0.3,"Dezful":0.3,"Khoy":0.3,"Bushehr":0.3 }

coords = { "Tehran":(35.6892,51.3890), "Mashhad":(36.2605,59.6168), "Isfahan":(32.6525,51.6776),
"Tabriz":(38.0700,46.2969), "Shiraz":(29.6100,52.5311), "Ahvaz":(31.3183,48.6706),
"Qom":(34.6416,50.8746), "Kermanshah":(34.3142,47.0650), "Urmia":(37.5553,45.0728),
"Zahedan":(29.4963,60.8629), "Rasht":(37.2808,49.5832), "Yazd":(31.8974,54.3569),
"Arak":(34.0917,49.7010), "Kerman":(30.2839,57.0788), "Bandar Abbas":(27.1964,56.2873),
"Hamedan":(34.7980,48.5150), "Sanandaj":(35.3095,46.9980), "Khorramabad":(33.4878,48.3558),
"Birjand":(32.8663,59.2211), "Sari":(36.5633,53.0601), "Bojnurd":(37.4747,57.3349),
"Gorgan":(36.8436,54.4390), "Zanjan":(36.6736,48.4787), "Qazvin":(36.2688,50.0041),
"Kashan":(33.9850,51.4576), "Ardabil":(38.2498,48.2933), "Babol":(36.5383,52.6780),
"Shahrekord":(32.3266,50.8571), "Dezful":(32.3830,48.3989), "Khoy":(38.5500,44.9500),
"Bushehr":(28.9234,50.8203) }

G = nx.Graph()
for n in nodes:
    G.add_node(n, population=population[n], coord=coords[n])

for i in range(len(nodes)):
    for j in range(i+1,len(nodes)):
        lat1, lon1 = coords[nodes[i]]
        lat2, lon2 = coords[nodes[j]]
        R = 6371
        dlat = radians(lat2-lat1)
        dlon = radians(lon2-lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
        c = 2*atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        G.add_edge(nodes[i], nodes[j], weight=distance)

def heuristic_k_median(G, k=7):
    nodes_list = list(G.nodes())
    centers = random.sample(nodes_list, k)
    improved = True
    while improved:
        improved=False
        for i,c in enumerate(centers):
            for candidate in nodes_list:
                if candidate in centers: continue
                new_centers = centers.copy()
                new_centers[i] = candidate
                total_new=sum(min(nx.dijkstra_path_length(G, city, center, weight='weight')*G.nodes[city]['population'] for center in new_centers) for city in G.nodes())
                total_old=sum(min(nx.dijkstra_path_length(G, city, center, weight='weight')*G.nodes[city]['population'] for center in centers) for city in G.nodes())
                if total_new<total_old:
                    centers[i]=candidate
                    improved=True
    return centers

@app.route("/compute")
def compute():
    centers=heuristic_k_median(G)
    total_weighted_distance=sum(min(nx.dijkstra_path_length(G, city, center, weight='weight')*G.nodes[city]['population'] for center in centers) for city in G.nodes())
    result={"centers":[{"name":c,"lat":G.nodes[c]["coord"][0],"lon":G.nodes[c]["coord"][1]} for c in centers],
            "weighted_distance":total_weighted_distance}
    return jsonify(result)

if __name__=="__main__":
    app.run(debug=True)