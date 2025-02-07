import logging
import warnings
#logging.disable(logging.INFO)
logging.getLogger("speechbrain.utils").setLevel(logging.ERROR) 
warnings.simplefilter(action='ignore', category=FutureWarning)

import torch
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.audio import Audio
from pyannote.core import Segment
from scipy.spatial.distance import cdist
from fastapi import FastAPI, Request, File, UploadFile, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import subprocess
import os
import io
import requests
from paho.mqtt import client as mqtt_client
from functions.secrets import *
from functions import *
import asyncio
from openai import OpenAI
from pyper import Pyper
import uvicorn
import time

os.environ["HF_HUB_OFFLINE"] = "1"

piper = Pyper(piper_model_path)

run_training_at_start = True # For rapid testing without the need to test the voice password, set to False, otherwise set it to True

# Initialise the web server
app = FastAPI()

def load_model():
    global reference_embedding
    global audio_processor
    global model
    reference_embedding = torch.load("reference_embeddings.pt")
    audio_processor = Audio(sample_rate=16000, mono="downmix")
    model = PretrainedSpeakerEmbedding(
        "speechbrain/spkrec-ecapa-voxceleb",
        device=torch.device("cpu")
    )
    
def is_your_voice(threshold=0.5):
    data = requests.get("http://127.0.0.0:12101/api/play-recording")
    with open("output.wav", 'wb') as f:
        f.write(data.content)  # Write the audio data to the file
    waveform, sample_rate = audio_processor('output.wav')
    test_embedding = model(waveform[None])
    distance = cdist(reference_embedding, test_embedding, metric="cosine")[0][0]
    os.remove("output.wav")  # Remove the temporary audio file
    print("WAV Data recorded.")
    if not distance < threshold:
        return False
    else:
        return True

# Server
@app.post("/handle-intent")
async def handle_intent(request: Request):
    global run_training_at_start    
    json_request = await request.json()
    print(json_request)
    intent = json_request["intent"]["name"]
    params = json_request["slots"]
    
    if "SENSITIVE" in intent:
        if not run_training_at_start:
            load_model()
            run_training_at_start = True
        if not is_your_voice():
            return {"speech": {"text": "Action locked by voice print."}}
        else:
            intent = intent.replace("SENSITIVE", "")  # Remove "SENSITIVE" from the intent name
    
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
            subprocess.run(["aplay", "-D", "default", "-f", "cd"], input=temp_file.read(), check=True)
            return {"message": "Audio played successfully"}
        except subprocess.CalledProcessError as e:
            return {"error": f"Error playing audio: {str(e)}"}

@app.post("/text-to-speech")
async def text_to_speech(request: Request):
    data = await request.body()
    data = data.decode()
    
    piper.save(data, "output.wav")
    
    with open("output.wav", 'rb') as audio_file:
        audio = audio_file.read()
        
    return Response(content=audio, media_type="media/wav")
    
    
def chatgpt_fallback():
    audio_data = requests.get("http://127.0.0.1:12101/api/play-recording")
    with open("tmp.wav", 'wb') as f:
        f.write(audio_data.content)  # Write the audio data to the file
    with open("tmp.wav", 'rb') as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    
    response = chatgpt("You are a fallback system for the Rhassy assistant, with the persona of Jarvis from Iron Man, but you cannot currently call any on device functions, although you can answer world questions. Answer with as short a repsonse as you can, always in English. When the user says terminate or some similar phrase, do not respond at all.", transcription.text)
    print(response)
    os.remove("tmp.wav")  # Remove the temporary audio file
    Say(response)

#GetMusicData()
#print("Server started.")

async def mqtt_subscribe():
    def on_mqtt_connect(client, userdata, flags, rc):
        client.subscribe("hermes/nlu/intentNotRecognized")

    def on_mqtt_message(client, userdata, msg):
        if msg.topic == "hermes/nlu/intentNotRecognized":
            print(msg.payload.decode())
            chatgpt_fallback()
    
    client = mqtt_client.Client()
    client.on_connect = on_mqtt_connect
    client.on_message = on_mqtt_message

    client.connect(mqtt_broker, mqtt_port)
    time.sleep(1)
    client.loop_start()

    while True:
        await asyncio.sleep(1)
    
@app.on_event("startup")
async def startup_event():
    start = time.time()
    if run_training_at_start:
        load_model()
    asyncio.create_task(mqtt_subscribe())
    print("Server started in " + str(time.time() - start) + "seconds.")


if __name__ == "__main__":
    print("Starting the server...")
    uvicorn.run(app, host="0.0.0.0", port=2010)