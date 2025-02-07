####################################################################################################################
# Imports
import subprocess
import platform
import time
from pynput.keyboard import Controller, Key
import webbrowser
import YouTubeMusicAPI
from ytmusicapi import YTMusic#, OAuthCredentials
from .secrets import *
import requests
import os
import psutil
import subprocess

####################################################################################################################
# Global Setup

ytmusic = YTMusic()
ytmusic = YTMusic('secrets/browser.json')

keyboard = Controller()

####################################################################################################################
# Global Variables


####################################################################################################################
# Functions
def Say(text=None, siteid="master"):
    requests.post("http://127.0.0.1:12101/api/text-to-speech", json=text)#, "siteId": siteid})

def GetBatteryPercentage():
    if platform.system() == "Linux":
        battery_info = subprocess.check_output(["acpi", "-b"]).decode("utf-8").splitlines()
        for battery in battery_info:
            if "unavailable" not in battery:
                battery_percentage = int(battery.split(":")[1].split(", ")[1].replace("%", ''))
        return f"Battery is at {str(battery_percentage)} percent"
    else:
        raise NotImplementedError("Battery Percentage Retrieval has not been implemented on Windows yet")

def LockScreen():
    if platform.system() == "Linux":
        subprocess.run(["systemctl", "suspend", "-i"])
    else:
        raise NotImplementedError("Screen Locking has not been implemented on Windows yet")
    
def UnlockScreen():
    if platform.system() == "Linux":
        subprocess.run(["loginctl", "unlock-session"])
    else:
        raise NotImplementedError("Screen Unlocking has not been implemented on Windows yet")
    
def Shutdown():
    if platform.system() == "Linux":
        subprocess.run(["shutdown", "-h", "now"])
    else:
        raise NotImplementedError("Shutting Down has not been implemented on Windows yet")
    
def Restart():
    if platform.system() == "Linux":
        subprocess.run(["reboot"])
    else:
        raise NotImplementedError("Restarting has not been implemented on Windows yet")
    
def PlayMusic(title=None, artist=None):
    query = ""
    if title is not None:
        query += title
        if artist is not None:
            query += " " + artist
    elif artist is not None:
        query += artist
    
    result = YouTubeMusicAPI.search(query)
    if result:
        webbrowser.open(result["url"])
        
def GetMusicData():        
    songs = ytmusic.get_library_songs(limit=1000)
    titles = "("
    artists = "("
    count = 0
    for song in songs:
        title = song['title'].lower().replace("'", "").replace("?", "").replace(":", "").replace(",", "").replace(".", "").replace(";", "").replace("&", "").replace("!", "").replace('’', '')
        artist = song['artists'][0]['name'].lower()
        
        subs = open("output/substitutions", "r").readlines()
        
        for sub in subs:
            if sub.split("|")[0].lower() == title:
                title = sub.split("|")[1].strip()
                break
    
        for sub in subs:
            if sub.split("|")[0].lower() == artist:
                artist = sub.split("|")[1].strip()
                break
        
        for i in range(3):
            if '(' in title or ")":
                if '(' in title and ')' in title:
                    title = title[:title.index('(')].strip() + title[title.index(')')+1:].strip()
            if '[' in title or ']' in title:
                if '[' in title and ']' in title:
                    title = title[:title.index('[')].strip() + title[title.index(']')+1:].strip()
        
        if title not in titles:
            if count != 0:
                titles += " | " + title
            else:
                titles += title
        
        if artist not in artists:
            if count != 0:
                artists += " | " + artist
            else:
                artists += artist
        
        count += 1
    
    titles += ")"
    artists += ")"
        
    #shutil.copyfile("output/titles", "~/.config/rhasspy/profiles/en/slots/titles.test")
    #shutil.copyfile("output/artists", "~/.config/rhasspy/profiles/en/slots/artists.test")
    slots = requests.get("http://127.0.0.1:12101/api/slots").json()
    slots["titles"] = [titles,]
    slots["artists"] = [artists,]
    requests.post("http://127.0.0.1:12101/api/slots?overwrite_all=true", json=slots).text
    #subprocess.run("cp ~/Code/rhasspy-intent-handler/output/titles ~/.config/rhasspy/profiles/en/slots/")
    #subprocess.run("cp ~/Code/rhasspy-intent-handler/output/artists ~/.config/rhasspy/profiles/en/slots/")
    print("Music data has been saved.")
    
    requests.post("http://127.0.0.1:12101/api/train")
    print("Rhasspy has been re-trained")
    
    return "Music data has been saved."

def PlayPauseMedia():
    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)
    
    return ""
        
def SkipMedia():
    keyboard.press(Key.media_next)
    keyboard.release(Key.media_next)
    
    return ""

def PreviousMedia():
    keyboard.press(Key.media_previous)
    keyboard.release(Key.media_previous)
    
    return ""

def VolumeUp():
    keyboard.press(Key.media_volume_up)
    keyboard.release(Key.media_volume_up)
    
    return ""

def VolumeDown():

    keyboard.press(Key.media_volume_down)
    keyboard.release(Key.media_volume_down)
    
    return ""

def CloseTab():
    keyboard.press(Key.ctrl)
    keyboard.press("w")
    keyboard.release("w")
    keyboard.release(Key.ctrl)
    
    return ""

def OpenApp(app):
    command = apps[app]["command"]
    subprocess.Popen(f"nohup {command} > /dev/null 2>&1 &", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
def CloseApp(app):
    if apps[app]['other_names'] != []:
        names = apps[app]['other_names']
        names.append(app)
    else:
        names = [app]
    for process in psutil.process_iter():
        for name in names:
            if name in process.name():
                print('Process found. Terminating it.')
                process.terminate()
                
def SetReminder(name, time=None):
    pass