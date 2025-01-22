import requests
from .secrets import api_url, access_token

def ChangeLightState(entity=None, state=None):
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    data = {"entity_id": entity}
    if state == "on":
        requests.post(api_url + "api/service/light/turn_on", headers=headers, json=data)
        print("Turning on " + str(entity))
        return "Turning on"
    elif state == "off":
        requests.post(api_url + "api/service/light/turn_off", headers=headers, json=data)
        print("Turning off " + str(entity))
        return "Turning off"
    elif state == "toggle":
        requests.post(api_url + "api/service/light/toggle", headers=headers, json=data)
        print("Toggling " + str(entity))
        return "Toggling"
    else:
        print("Invalid state")

def ChangeCoverState(entity=None, state=None):
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    data = {"entity_id": entity}
    if state == "open":
        requests.post(api_url + "api/service/cover/open_cover", headers=headers, json=data)
        print("Opening " + str(entity))
        return "Opening"
    elif state == "close":
        requests.post(api_url + "api/service/cover/close_cover", headers=headers, json=data)
        print("Closing " + str(entity))
        return "Closing"
    elif state == "toggle":
        requests.post(api_url + "api/service/cover/toggle", headers=headers, json=data)
        print("Toggling " + str(entity))
        return "Toggling"
    else:
        print("Invalid state")