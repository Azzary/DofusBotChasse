zaap = """Amakna (château d'Amakna)/t[3,-5]
Amakna (village d'Amakna)/t[-2,0]
Amakna (Montagne des Craqueleurs)/t[-5,-8]
Amakna (Orée de la forêt maléfique)/t[-1,13]
Amakna (Coin Bouftou)/t[5,7]
Amakna (port de Madrestam)/t[7,-4]
Amakna (Plaine des Scarafeuilles)/t[-1,24]
Archipel des Écailles (Crocuzko)/t[-83,-15]
Astrub (Cité d'Astrub)/t[5,-18]
Bonta (centre-ville)/t[-32,-56]
Brâkmar (centre-ville)/t[-26,35]
Plaines de Cania (Lac de Cania)/t[-3,-42]
Plaines de Cania (Massif de Cania)/t[-13,-28]
Plaines de Cania (village des diablotins)/t[-16,-24]
Plaines de Cania (village de Kanig)/t[0,-56]
Plaines de Cania (Plaine de cochon moche)/t[-5,-23]
Plaines de Cania (plaines rocheuses)/t[-17,-47]
Plaines de Cania (routes rocheuses)/t[-20,-20]
Plaines de Cania (Les Champs de Cania)/t[-27,-36]
Profondeurs d'Astrub (Arc de Vili)/t[15,-20]
Territoire Dopple (Village Dopple)/t[-34,-8]
Ile de Frigost (Entrée du Château d'Harebourg)/t[-67,-75]
Île de Frigost (Village de Frigost)/t[-78,-41]
Île de Frigost (village enneigé)/t[-77,-73]
Koalak Mountain (Village des éleveurs)/t[-16,1]
L'île de la Lune (Tortue Beach)/t[35,12]
Ohwymi (Dunes des ossements)/t[15,-58]
Île d'Otomaï (village de la canopée)/t[-54,16]
Île d'Otomaï (village côtier)/t[-46,18]
Île de Pandala (village de Pandala)/t[20,-29]
Landes de Sidimote (allée des caravanes)/t[-25,12]
Landes de Sidimote (Hautes Terres Profanées)/t[-15,25]
Baie de Sufokia (Temple de l'Alliance)/t[13,35]
Baie de Sufokia (Sufokia)/t[13,26]
Baie de Sufokia (Rivage Sufokien)/t[10,22]
Tainela (Le Berceau)/t[1,-32]
Îles Wabbit (Labowatowies abandonnées)/t[27,-14]
Îles Wabbit (Île Cawotte)/t[25,-4]
Le village de Zoth (Village de Zoth)/t[-53,18]"""

# create a json file with the coordinates
import json
import os
import sys


def create_json(zaap):
    zaap_list = zaap.split('\n')
    zaap_dict = {}
    for zaap in zaap_list:
        zaap_coord = zaap.split('/t')
        zaap_coord[1] = zaap_coord[1][1:-1]
        zaap_coord[0] = zaap_coord[0].split('(')[1].split(')')[0]
        zaap_dict[zaap_coord[0]] = {'x': int(zaap_coord[1].split(',')[0]), 'y': int(zaap_coord[1].split(',')[1])}
    with open('zaap.json', 'w') as f:
        json.dump(zaap_dict, f)



# get the zaap closer to a x,y pos
def get_zaap(x, y):
    with open('zaap.json') as f:
        zaap_dict = json.load(f)
    best_zaap = None
    best_distance = 10000
    for zaap in zaap_dict:
        zaap_coord = zaap_dict[zaap]
        distance = abs(zaap_coord['x'] - x) + abs(zaap_coord['y'] - y)
        if distance < best_distance:
            best_zaap = {"name": zaap,"coor": zaap_dict[zaap], 'distance': distance}
            best_distance = distance
    return best_zaap