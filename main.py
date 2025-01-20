from fastapi import FastAPI, Request, File, UploadFile
import subprocess
import io
from functions import *

app = FastAPI()

def ChangeLightColor(color=None, name=None):
    print(color, name)

@app.post("/handle-intent")
async def handle_intent(request: Request):
    json_request = await request.json()
    print(json_request)
    print(globals())
    intent = json_request["intent"]["name"]
    params = json_request["slots"]
    if params != {}:
        response = globals()[intent](**params)
    else:
        response = globals()[intent]()
    if response == None:
        response = ""
    return {"speech": {"text": response}}

@app.post("/play-audio")
async def play_audio(request: Request):
    # Get raw audio data from the request body
    audio_data = await request.body()

    with io.BytesIO(audio_data) as temp_file:
        # Use subprocess to call aplay and play the wav data from the temporary file
        temp_file.seek(0)  # Reset file pointer to the beginning
        try:
            # Use aplay to play the audio data from the file
            subprocess.run(["aplay", "-f", "cd"], input=temp_file.read(), check=True)
            return {"message": "Audio played successfully"}
        except subprocess.CalledProcessError as e:
            return {"error": f"Error playing audio: {str(e)}"}