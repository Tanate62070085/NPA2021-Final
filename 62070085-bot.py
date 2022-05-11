
import json
from multiprocessing.connection import wait
import time
from urllib import response
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
requests.packages.urllib3.disable_warnings()

def request_interface(interface="GigabitEthernet1"):
    api_url = "https://10.0.15.102/restconf/data/ietf-interfaces:interfaces/interface="+interface

    headers = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }

    basicauth = ("admin", "cisco")
    resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)
    response_json = resp.json()
    return response_json


"""Key 12 hours"""
def sent_to_room(token,roomid,text):
    """sent text to room Webex api"""
    m = MultipartEncoder({'roomId': roomid,
                      'text': text})
    r = requests.post('https://webexapis.com/v1/messages', data=m,
                  headers={'Authorization': 'Bearer ' + token,
                  'Content-Type': m.content_type})
    return(r.text)
    

def get_from_room(token,roomid):
    """sent text to room Webex api"""
    m = MultipartEncoder({'roomId': roomid})
    r = requests.get('https://webexapis.com/v1/messages',data=m,
                  headers={'Authorization': 'Bearer ' + token,
                  'Content-Type': m.content_type,
                  },params={'roomId': roomid})
    return(r.json())

def enable_interface(interface):
    api_url = "https://10.0.15.102/restconf/data/ietf-interfaces:interfaces/interface="+interface

    headers = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }
    basicauth = ("admin", "cisco")

    body = json.dumps({
        "ietf-interfaces:interface":{
            "enabled": True
        }      
    })
    response = requests.patch(api_url, auth=basicauth, headers=headers, verify=False, data=body)
    print(response.text)


def Bot_main():
    key = open("Important-key.json")
    data = json.load(key)
    token = data["token"]
    roomid = data["roomid"]
    key.close()
    interface_status = request_interface("Loopback62070085")
    print(interface_status["ietf-interfaces:interface"]["enabled"])
    message = get_from_room(token,roomid)["items"][0]["text"]
    try:
        while True:
            if message == "62070085":
                interface_status = request_interface("Loopback62070085")
                interface_status = interface_status["ietf-interfaces:interface"]["enabled"]
                if interface_status:
                    interface_status = "up"
                    sent_to_room(token,roomid,"Enable Loopback62070085 - Now the Operational status is up again")
                else:
                    interface_status = "down"
                    sent_to_room(token,roomid,"Enable Loopback62070085 - Now the Operational status is still down")
                # sent_to_room(token,roomid,"Loopback62070085 - Operational status is "+interface_status)
            time.sleep(1)
            message = get_from_room(token,roomid)["items"][0]["text"]
    except KeyboardInterrupt:
        print("Stop")
        pass
Bot_main()
# enable_interface("Loopback62070085")
