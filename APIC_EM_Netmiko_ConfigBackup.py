#!/usr/bin/env python
#
import requests
import json
from netmiko import ConnectHandler


requests.packages.urllib3.disable_warnings() # Disable warnings

# APIC-EM IP, modify these parameters if you are using your own APIC-EM
apicem_ip = "apic-em.fullyqualifiedORip.com"
username = "admin"
password = "cisco"
version = "v1"

# setting username and password
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
r = requests.get('https://apic-em.bhmlab.ciscolabs.com/api/v1/network-device', headers=headers,verify=False)
#print ("Request Status: ",resp.status_code)
response_json = r.json()
#print response_json
device = response_json["response"]
#uncomment for testing
#print(json.dumps(device,indent=4))

#Define the List for our Device Inventory
device_list = []
#Loop through APIC-EM's device inventory and grab hostname, IP, and APIC-EMs unique device id element
for item in device:
    fam = ([item['family']])
    strFam = ''.join(fam)
    hostName = ([item['hostname']])
    strHost = ''.join(hostName)
    IP = ([item['managementIpAddress']])
    strIP = ''.join(IP)
    id = ([item["id"]])
    strId = ''.join(id)
    print "**************************************"
    print strHost,(","),strIP,(","),strFam
    print "**************************************"
    #define netmiko connection handler with IP address entry from our APIC Device Inventory
    cisco_CSR = {
        'device_type': 'cisco_ios',
        'ip': '%s' %strIP,
        'username': 'admin',
        'password': 'cisco',
        'secret' : 'cisco',
        }

    #connect to the device
    net_connect = ConnectHandler(**cisco_CSR)
    #enable exec mode
    net_connect.enable()
    #run the "show run" command on the cli and capture the output
    output1 = net_connect.send_command("sh run")
    #print output1
    #define filename with hostname variable
    filename = "ConfigurationBackup_%s.txt" % strHost
    print '>>',filename

    #write configuration to file
    with open(filename, 'w') as f:
        f.write(output1)

    #upload file to APIC-EM PNP
    url = "https://" + apicem_ip + "/api/v1/file/config"
    file = {filename : open(filename,'rb')}
    res = requests.post(url, headers=headers, files=file, verify=False)
