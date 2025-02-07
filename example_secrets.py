# Place me in functions and name me secrets.py 
# I don't know why I'm using a python file instead of YAML or JSON, but I just decided to keep it simple.

home_assistant_url = "http://homeassistant:8123/" # Make sure there's a / at the end.
access_token = "" # From Home Assistant https://developers.home-assistant.io/docs/api/rest/
voice_password = "peter rabbit and mario" # The phrase used for your voice password, also needs to be configured in Rhasspy to point to UnlockScreenSENSITIVE
mqtt_broker = "localhost" # Point to the same MQTT broker that Rhasspy uses.
mqtt_port = 12183 # Rhasspy uses port 12183 by default for MQTT.
openai_api_key = "" # API key used for smart fallback from OpenAI.
piper_model_path = "/home/james/Piper/jarvis-high.onnx" # Path for the piper model used for TTS.
owm_api_key = "" # OpenWeatherMap API key.
owm_lat = 90 # Latitude for OpenWeatherMap location.
owm_lon = 45 # Longitude for OpenWeatherMap location.
email = "example@example.com" # Email for simplegmail email checking
email_password = "3" # App password for simplegmail email checking.

# This is a list of apps that can be opened and closed by Rhasspy.
apps = {"kicad": {"other_names": [], "command": "flatpak run org.kicad.KiCad", "can_close": True, "close_command_run": "/app/bin/kicad"},
        "teams": {"other_names": [], "command": "flatpak run com.github.IsmaelMartinez.teams_for_linux", "can_close": True, "close_command_run": "/app/teams-for-linux/teams-for-linux"},
        "firefox": {"other_names": [], "command": "snap run firefox", "can_close": True, "close_command_run": "/snap/firefox/5647/usr/lib/firefox/firefox"},
        "vscode": {"other_names": ["code"], "command": "code", "can_close": False, "close_command_run": ""},
        "discord": {"other_names": [], "command": "flatpak run com.discordapp.Discord", "can_close": True, "close_command_run": "/app/discord/Discord"},
        "onenote": {"other_names": [], "command": "flatpak run com.patrikx3.onenote", "can_close": True, "close_command_run": "/app/lib/com.patrikx3.onenote/p3x-onenote"},
        "brave": {"other_names": [], "command": "brave-browser", "can_close": True, "close_command_run": "/bin/bash /usr/bin/brave-browser-stable"},
        "thonny": {"other_names": [], "command": "thonny", "can_close": True, "close_command_run": "/usr/bin/python3 /usr/bin/thonny"}
        } # You only really need the "other_names" and "command" attributes, the others are from previous versions of the code.