import requests
import json
import urllib,requests
import random

s = requests.Session()
import time,random
def postmess(number,fromn,text):
        params = {
        'api_key': '',
        'api_secret': '',
        'to': number,
        'from': fromn,
        'text':  text,
        'type': 'unicode'
        }
        url = 'https://rest.nexmo.com/sms/json?' + urllib.parse.urlencode(params)


        headers = {'Accept': 'application/json'}
        print(requests.get(url,headers=headers).text)

tm = time.time()
contacts = ["972XXXXXXX"]
import requests
def append_lottry_tofile(lottery_id):
    ff = open("data.json","r")
    data = json.loads(ff.read())
    ff.close()
    if lottery_id not in data:
        data.append(lottery_id)
        ff = open("data.json","w")
        ff.write(json.dumps(data))
        ff.close()
def get_lottry_ids():
    ff = open("data.json","r")
    data = json.loads(ff.read())
    return data


results = []
num = 0
for x in range(1,3):
    try:
        temp = json.loads(requests.get("https://www.dira.moch.gov.il/api/Invoker?method=Projects&param=%3FfirstApplicantIdentityNumber%3D%26secondApplicantIdentityNumber%3D%26ProjectStatus%3D1%26Entitlement%3D1%26PageNumber%3D"+str(x)+"%26PageSize%3D12%26",timeout=10000).text)
        if x == 1:
            num = temp["OpenLotteriesCount"]
        for lott in temp["ProjectItems"]:
            if lott["IsLotteryHeld"] == False:
                results.append(lott)
    except:
        print("ccc")
        break

if num == 0:
    print("no open")
    exit()
message = ""
cities = []
allreadydone = get_lottry_ids()
for lottery in results:
    if lottery["CityDescription"] not in cities and lottery["LotteryNumber"] not in allreadydone:
        cities.append(lottery["CityDescription"])
message = """הגרלות חדשות ב:""" + ", ".join(cities)
if len(cities) > 0:
    for contact in contacts:
        postmess(contact,"TZAHI",message + """
        https://www.dira.moch.gov.il/ProjectsList""")
for lottery in results:
    append_lottry_tofile(lottery["LotteryNumber"])


projects = []
#print(num["CityDescription"])

