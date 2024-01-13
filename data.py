import json
import os
import requests
import urllib.parse
import urllib.request
from settings import API_KEY, query

#champion cdn version check urls
CDN_VER_CHECK_URL = "https://ddragon.leagueoflegends.com/api/versions.json"
CDN_VER = json.load(urllib.request.urlopen(CDN_VER_CHECK_URL))[0]
CDN_URL = 'https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(CDN_VER)

# check if championlist.json is present and up to date
if os.path.isfile('championlist.json'):
    with open("championlist.json", "r") as read_content: 
        champs = json.load(read_content)
        flag = False
    if champs['version'] != CDN_VER:
        print("Updating champs")
        flag = True
else:
    print("Making champs list")
    flag = True

# update/make champs list
if flag:
    with urllib.request.urlopen(CDN_URL) as url:
        champs_raw = json.load(url)
    champs = {'version': CDN_VER}
    for champ,stuff in champs_raw['data'].items():
        champs[stuff['key']] = champ
    json.dump(champs, open('championlist.json', 'w'))

print('patch ', CDN_VER)

#API error class
class RiotAPIError(Exception):
    pass

def masteries_json(gameName, tag, reg) -> list:
    # riot api
    URL = "https://{{region}}.api.riotgames.com/{{req}}?api_key={key}"

    # riot api-key from settings.py
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
    r = requests.get(URL.format(
        region = reg, 
        req = masteries.format(ppuid=ppuid)))

    if r.status_code != 200:
        raise RiotAPIError("Error: "+ str(r.status_code)+" masteries")

    #success message
    print('RiotID: {}#{} from {} loaded'.format(gameName, tag, reg))
    return r.json()

data = masteries_json(query.gameName, query.tag, query.reg)