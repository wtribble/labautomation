#!/usr/bin/env python
#

import requests
import json



requests.packages.urllib3.disable_warnings() # Disable warnings

# APIC-EM IP, modify these parameters if you are using your own APIC-EM
apicem_ip = "sandboxapic.cisco.com"
username = "devnetuser"
password = "Cisco123!"
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
print ("Request Status: ",resp.status_code)

#store ticket in a variable
x_auth_token = resp.json()["response"]["serviceTicket"]

#create get request header
headers = {"X-Auth-Token": x_auth_token}
#print headers

get_url = "https://"+apicem_ip+"/api/v1/network-device"
#
r = requests.get(get_url, headers=headers,verify=False)
#print ("Request Status: ",resp.status_code)
response_json = r.json()
#print response_json
device = response_json["response"]
#uncomment for testing
#print(json.dumps(device,indent=4))

device_list = []
#extract data from json

for item in device:
    fam = ([item['family']])
    strFam = ''.join(fam)
    hostName = ([item['hostname']])
    strHost = ''.join(hostName)
    id = ([item["id"]])
    strId = ''.join(id)
    if strFam == "Routers" or strFam == 'Switches and Hubs':
        print "**************************************"
        print strHost,(","),strFam
        print "**************************************"
        print "portName||ifIndex||adminStatus||ipv4Address||macAddress||vlanId||description"
        url = "https://"+apicem_ip+"/api/v1/interface/network-device/%s" % strId
        v = requests.get(url, headers=headers,verify=False)
        intResp_json = v.json()
        int = intResp_json["response"]
        #print (json.dumps(int,indent=4))
        interface_list = []
   #     extract data from jso
        for item in int:
            print ('{}||{}||{}||{}||{}||{}||{}'.format(item['portName'],item['ifIndex'],item['adminStatus'],item['ipv4Address'],item['macAddress'],item['vlanId'],item['description']))
