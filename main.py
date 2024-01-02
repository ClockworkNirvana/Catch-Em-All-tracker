import json
import matplotlib.pyplot as plt
import numpy as np
import os
import requests
import urllib.parse
import urllib.request

#champion cdn version v13.24
CDN_VER = '13.24.1'
CDN_URL = 'https://ddragon.leagueoflegends.com/cdn/13.24.1/data/en_US/champion.json'
if os.path.isfile('champion.json') == False:
    with urllib.request.urlopen(CDN_URL) as url:
        champs = json.load(url)
        json.dump(champs, open('champion.json', 'w'))
else:
    with open("champion.json", "r") as read_content: 
        champs = json.load(read_content)
    if champs['version'] != CDN_VER:
        print("New champion.json version detected. Updating...")
        with urllib.request.urlopen(CDN_URL) as url:
            champs = json.load(url)
            json.dump(champs, open('champion.json', 'w'))

print('patch ', CDN_VER)

#API error class
class RiotAPIError(Exception):
    pass

def masteries_json(gameName, tag, reg) -> list:
    # riot api-endpoint
    URL = "https://{{region}}.api.riotgames.com/{{req}}?api_key={key}"

    # riot api-key changes every 24 hrs
    API_KEY = "RGAPI-522a5bab-26a7-4101-83d2-16674ce38b54"
    URL = URL.format(key=API_KEY)

    # api locations
    # get ppuid from riot id
    by_id = "riot/account/v1/accounts/by-riot-id/{gameName}/{tag}"
    PARAMS_BY_ID = {'gameName':gameName, 'tag':tag}

    #escapes ids
    PARAMS_BY_ID = {x:urllib.parse.quote(y) for x,y in PARAMS_BY_ID.items()}
    by_id = by_id.format(**PARAMS_BY_ID)

    # get request for ppuid from riot id
    r = requests.get(URL.format(region = 'asia', req=by_id))
    if r.status_code != 200:
        raise RiotAPIError("Error: "+ str(r.status_code)+" ppuid")
    ppuid = r.json()['puuid']

    # get champ masteries
    masteries = "lol/champion-mastery/v4/champion-masteries/by-puuid/{ppuid}"
    r = requests.get(URL.format(region = reg, req=masteries.format(ppuid=ppuid)))

    if r.status_code != 200:
        raise RiotAPIError("Error: "+ str(r.status_code)+" masteries")

    print('RiotID:', gameName+'#'+tag, 'from', reg, 'loaded')
    return r.json()

data = masteries_json('KPG Clockwork','SG2','sg2')

class champion:
    def __init__(self, id, level, points):
        self.id = id
        self.level = level
        self.points = points

masteries = []

for thing in data:
    masteries.append(champion(thing['championId'], thing['championLevel'], thing['championPoints']))



# Commented out as per instruction
# for 

# x_data = list(range(1, jumps+2))
# y_data = data_gen(simulations, jumps, probability)
# fig = plt.figure(figsize=(10, 5))

# plt.bar(x_data, data_gen(simulations, jumps, probability))

# plt.xlabel("Position")
# plt.ylabel("Probability")
# plt.suptitle("Probability distribution of the jumper landing on a given position from the left")
# plt.title("P(jumps left) = {}, Num of jumps = {}, P(jump left on 1st jump) = {}".format(probability, jumps, 0.5))
# plt.show()