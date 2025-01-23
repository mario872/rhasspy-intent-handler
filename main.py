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
from fastapi import FastAPI, Request, File, UploadFile
import subprocess
import os
import io
import requests
from functions import *

run_training_at_start = True # Set to True if you don't intend to edit these files very often, otherwise set to False

# Initialise the web server
app = FastAPI()

def train_model():
    global model
    global audio_processor
    global reference_embedding
    print("Initialising speaker verification model and audio processing...")
    # Initialize the speaker embedding model
    model = PretrainedSpeakerEmbedding(
        "speechbrain/spkrec-ecapa-voxceleb",
        device=torch.device("cpu")
    )
    audio_processor = Audio(sample_rate=16000, mono="downmix")

    reference_audio_files = os.listdir("voice_input")
    if "placeholder.txt" in reference_audio_files:
        reference_audio_files.remove("placeholder.txt")
    embeddings = []
    for audio_file in reference_audio_files:
        waveform, sample_rate = audio_processor("voice_input/" + audio_file)
        embedding = model(waveform[None])
        # Convert numpy.ndarray to torch.Tensor
        embeddings.append(torch.tensor(embedding))
    reference_embedding = torch.mean(torch.stack(embeddings), dim=0)
    print("Reference embeddings loaded.")

if run_training_at_start:
    train_model()

def is_your_voice(threshold=0.4):
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
            train_model()
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
    
GetMusicData()
print("Server started.")