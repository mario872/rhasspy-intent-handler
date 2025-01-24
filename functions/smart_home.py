import requests
from .secrets import api_url, access_token

def ChangeLightState(entity=None, state=None):
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    data = {"entity_id": entity}
    if state == "on":
        resp = requests.post(api_url + "api/services/light/turn_on", headers=headers, json=data)
        print("Turning on " + str(entity) + " with status code: " + str(resp.status_code))
        return "Turning on"
    elif state == "off":
        resp = requests.post(api_url + "api/services/light/turn_off", headers=headers, json=data)
        print("Turning off " + str(entity) + " with status code: " + str(resp.status_code))
        return "Turning off"
    elif state == "toggle":
        resp = requests.post(api_url + "api/services/light/toggle", headers=headers, json=data)
        print("Toggling " + str(entity) + "with status code: " + str(resp.status_code))
        return "Toggling"
    else:
        print("Invalid state")

def ChangeCoverState(entity=None, state=None):
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    data = {"entity_id": entity}
    if state == "open":
        resp = requests.post(api_url + "api/services/cover/open_cover", headers=headers, json=data)
        print("Opening " + str(entity) + " with status code: " + str(resp.status_code))
        return "Opening"
    elif state == "close":
        resp = requests.post(api_url + "api/services/cover/close_cover", headers=headers, json=data)
        print("Closing " + str(entity) + " with status code: " + str(resp.status_code))
        return "Closing"
    elif state == "toggle":
        resp = requests.post(api_url + "api/services/cover/toggle", headers=headers, json=data)
        print("Toggling " + str(entity) + "with status code: " + str(resp.status_code))
        return "Toggling"
    else:
        print("Invalid state")