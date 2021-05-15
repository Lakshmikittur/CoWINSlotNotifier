#!/usr/bin/env python3

import requests
import json
import sib_api_v3_sdk
from sib_api_v3_sdk.models.send_smtp_email import SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException
from datetime import datetime



# Setup Send In Blue client to send email
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = 'xkeysibdajdbajfvajfasldkodioq78qtrqyhbqdqdyqdvqoidgqcqq9' #API keys from Send In Blue. Keep this secret



# File that contains data regarding users and their districts that should be monitored to get slot info
EmailIDsFileName = "AllEmailData.json"
emailData = []
with open(EmailIDsFileName,"r") as fs:
    emailData = json.load(fs)



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
        return False



# Function to use sib APIs to send email once slot is available
def send_email(emailid, content):
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=emailid, subject="Slot available by Laksh", params={"CONTENT": content},template_id=5, headers={"X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3", "charset": "iso-8859-1"}) # SendSmtpEmail | Values to send a transactional email
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Sent email to: {emailid}")
        print(api_response)
        return True
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        return False



# Main part to see if slots are available or not and if already notfied user then refrain from notify again for certain time period
for distr in emailData:
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
                    content += "     "
                if send_email(distr['emails'],content):
                    distr['LastSentTime'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    IfSent = True
            break
        distr['CentersNotified'] = [x['name'] for x in result]



# Save the updated data
with open(EmailIDsFileName,"w") as fs:
    json.dump(emailData,fs,indent=4)
