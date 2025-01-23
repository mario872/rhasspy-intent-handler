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

####################################################################################################################
# Global Setup

ytmusic = YTMusic()
ytmusic = YTMusic('secrets/browser.json')

keyboard = Controller()

####################################################################################################################
# Global Variables


####################################################################################################################
# Functions
def Say(text=None, siteid="default"):
    requests.post("http://127.0.0.1:12101/api/text-to-speech", json={"text": text, "siteId": siteid})
        
def SaveVoiceClip(location="./", index=None):
    requests.post("http://127.0.0.1:12101/api/listen-for-command?nohass=True")
    
    data = requests.get("http://127.0.0.1:12101/api/play-recording")
    if index is not None:
        filename = "audio" + str(index)
    else:
        filename = "audio"
    with open(location + filename + ".wav", 'wb') as f:
        f.write(data.content)  # Write the audio data to the file

def GetBatteryPercentage():
    if platform.system() == "Linux":
        battery_info = subprocess.check_output(["acpi", "-b"]).decode("utf-8").splitlines()
        for battery in battery_info:
            if "unavailable" not in battery:
                battery_percentage = int(battery_info.split(":")[1].split(", ")[1])
        return battery_percentage
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
    
    with open("output/titles", 'w') as f:
        f.writelines(titles)
    
    with open("output/artists", 'w') as f:
        f.writelines(artists)
        
    "cp ~/Code/rhasspy-intent-handler/output/titles ~/.config/rhasspy/profiles/en/slots/titles"
    "cp ~/Code/rhasspy-intent-handler/output/artists ~/.config/rhasspy/profiles/en/slots/artists"
    print("Music data has been saved.")
    return "Music data has been saved."

def PlayPauseMedia():
    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)
    
    return ""
        