#!/usr/bin/env python3

import requests
import json
from datetime import datetime



# File that contains data regarding users and their districts that should be monitored to get slot info
DistrictsDataFileName = "DistrictsData.json"
districtData = []
with open(DistrictsDataFileName,"r") as fs:
    districtData = json.load(fs)



# Function to get availability of slots within next 7 days in a particular district
def getDetailsByDistrict(district_id, date):
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    
    response = requests.get(url, params={"district_id":district_id,"date":date}, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"})
    if response.status_code == 200:
        rep = response.json()
        result=[]
        for center in rep["centers"]:
            for session in center["sessions"]:
                if session["min_age_limit"] < 45 and session["available_capacity"] > 0:
                    result.append({"name":center['name'] , "capacity":session['available_capacity'] ,"date":session['date']})
        return sorted(result, key=lambda k:k['date'])
    else:
        print('Can not contact to API server')
        return False



# Main part to see if slots are available or not and if already notfied user then refrain from notify again for certain time period
for distr in districtData:
    cDate = datetime.now().strftime("%d-%m-%Y")
    result = getDetailsByDistrict(distr["id"],cDate)
    if result != False and len(result) > 0:
        storedTime = datetime.now()
        if distr["LastSentTime"] != "":
            storedTime = datetime.strptime(distr["LastSentTime"],"%d/%m/%Y %H:%M:%S")
        for citem in result:
            if citem['name'] not in distr['CentersNotified'] or (datetime.now() - storedTime).total_seconds() >= 14400:
                content = "\n"
                for item in result:
                    content = f"{content}{item['name']} has {item['capacity']} seats on {item['date']}"
                    content += "\n"
                print(content)
                distr['LastSentTime'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            break
        distr['CentersNotified'] = [x['name'] for x in result]
    else:
        print("Can not find open slot")



# Save the updated data
with open(DistrictsDataFileName,"w") as fs:
    json.dump(districtData,fs,indent=4)
