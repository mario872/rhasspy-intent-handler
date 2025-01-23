# FAQ
**ImportError: this platform is not supported: ("failed to acquire X connection: No module named 'Xlib'", ModuleNotFoundError("No module named 'Xlib'"))**
`sudo apt-get install python3-xlib` or `python -m pip install xlib`

**What is browser.json?!**
browser.json is the file that provides the YouTube Music API with the browser token used to authenticate you as yourself. [Instructions](https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html)

**docker: unknwon server OS: .**
The docker daemon has not been started yet, or you need to use sudo.

**What is the voice_input folder for?**
Place some recordings of your voice around five seconds each to then train to test if other recordings are your voice. I find that one or two words are usually not enough to verify a voice, so you may need to say the one or two words you later want to verify, e.g. for a voice password.