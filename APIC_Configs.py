#!/usr/bin/env python
#

import requests
import json
from tabulate import tabulate

requests.packages.urllib3.disable_warnings() # Disable warnings

# APIC-EM IP, modify these parameters if you are using your own APIC-EM
apicem_ip = "apic-em.fullyqualifiedORip.com"
username = "admin"
password = "cisco"
version = "v1"

# JSONhttps://sandboxapic.cisco.com/ input
r_json = {
    "username": username,
    "password": password
}

# POST ticket API URL
post_url = "https://"+apicem_ip+"/api/"+version+"/ticket"

# All APIC-EM REST API request and response content type is JSON.
headers = {'content-type': 'application/json'}
#print headers

# Make request and get response - "resp" is the response of this request
resp = requests.post(post_url, json.dumps(r_json), headers=headers,verify=False)
#print ("Request Status: ",resp.status_code)

#store ticket in a variable
x_auth_token = resp.json()["response"]["serviceTicket"]

#create get request header
headers = {"X-Auth-Token": x_auth_token}
#print headers

#
r = requests.get('https://apic-em.bhmlab.ciscolabs.com/api/v1/network-device/config', headers=headers,verify=False)
#print ("Request Status: ",resp.status_code)
response_json = r.json()
#print response_json
device = response_json["response"]
#uncomment for testing
print(json.dumps(device,indent=4))
