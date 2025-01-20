from homeassistant_api import Client
from .secrets import api_url, access_token

def ChangeLightState(entity=None, state=None):
    with Client(api_url, access_token) as client:
        light = client.get_domain("light")
        if state == "on":
            light.turn_on(entity_id=entity)
            print("Turning on " + str(entity))
            return "Turning on"
        elif state == "off":
            light.turn_off(entity_id=entity)
            print("Turning off " + str(entity))
            return "Turning off"
        elif state == "toggle":
            light.toggle(entity_id=entity)
            print("Toggling " + str(entity))
            return "Toggling"
        else:
            print("Invalid state")

def ChangeCoverState(entity=None, state=None):
    with Client(api_url, access_token) as client:
        cover = client.get_domain("cover")
        if state == "open":
            cover.open_cover(entity_id=entity)
            print("Opening " + str(entity))
            return "Opening"
        elif state == "close":
            cover.close_cover(entity_id=entity)
            print("Closing " + str(entity))
            return "Closing"
        elif state == "toggle":
            cover.toggle(entity_id=entity)
            print("Toggling " + str(entity))
            return "Toggling"
        else:
            print("Invalid state")