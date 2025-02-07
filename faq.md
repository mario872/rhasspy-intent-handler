# FAQ
**ImportError: this platform is not supported: ("failed to acquire X connection: No module named 'Xlib'", ModuleNotFoundError("No module named 'Xlib'"))**
`sudo apt-get install python3-xlib` or `python -m pip install xlib`

**What is browser.json?!**
browser.json is the file that provides the YouTube Music API with the browser token used to authenticate you as yourself. [Instructions](https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html)

**docker: unknwon server OS: .**
The docker daemon has not been started yet, or you need to use sudo.

**What is the voice_input folder for?**
Place some recordings of your voice around five seconds each to then train to test if other recordings are your voice. I find that one or two words are usually not enough to verify a voice, so you may need to say the one or two words you later want to verify, e.g. for a voice password.

**What is train.py for?**
This script is used to get audio recordings of your voice and then used to train a model to recognise those recordings.
Usage: `python3 train.py --train-model` will train and save the model, `python3 train.py --save-voice-password` will only record for the voice password. It will record over previous voice password recordings if they exist. `python3 train.py --save-clips` will record the voice password and a few extra clips for training, like shutdown, restart and reboot.

**pyowm.commons.exceptions.UnauthorizedError: Invalid API Key provided**
Either, you need to register a new API key, as legacy ones have been blocked from using the One Call API v3.0. Or you need to edit `python3.version/site-packages/pyowm/weatherapi25/uris.py`. Change the line that says: `ROOT_WEATHER_API = 'openweathermap.org/data/2.5'` to `ROOT_WEATHER_API = 'openweathermap.org/data/2.5'`