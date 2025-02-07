from functions.secrets import voice_password
from notifypy import Notify
import time
from num2words import num2words
import argparse
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.audio import Audio
from pyannote.core import Segment
import os
import torch
import requests

os.environ["HF_HUB_OFFLINE"] = "0"

parser = argparse.ArgumentParser(description='Train the voice password and speaker verification model.')
parser.add_argument('--save-clips', action='store_true', help='Save voice clips for the voice password and the speaker verification model.')
parser.add_argument('--save-voice-password', action='store_true', help='Save clips for the voice password.')
parser.add_argument('--train-model', action='store_true', help='Train the speaker verification model.')
args = parser.parse_args()

def SaveVoiceClip(location="./", index=None):
    requests.post("http://127.0.0.1:12101/api/listen-for-command?nohass=True")
    
    data = requests.get("http://127.0.0.1:12101/api/play-recording")
    if index is not None:
        filename = "audio" + str(index)
    else:
        filename = "audio"
    with open(location + filename + ".wav", 'wb') as f:
        f.write(data.content)  # Write the audio data to the file

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
    with open("reference_embeddings.pt", "wb") as f:
        torch.save(reference_embedding, f)  # Save the reference embeddings for future use
    print("Reference embeddings loaded.")

def TrainVoicePassword():
    print("Make sure to specify your voice_password in the functions/secrets.py file.")
    for _ in range(5):
        print(voice_password + "\nPress ENTER to start recording.")
        input()
        SaveVoiceClip(location="voice_input/", index=_)

def TrainSpeakerVerificationModelAndPassword():
    TrainVoicePassword()
    
    sentences = []
    for i in range(3):
        sentences.append("shutdown")
        sentences.append("restart")
        sentences.append("reboot")
    
    print(f"You will say {num2words(len(sentences))} different sentences, and your voice password five times.")
    i = 5
    for sentence in sentences:
        print(sentence + "\nPress ENTER to start recording.")
        input()
        SaveVoiceClip(location="voice_input/", index=i)
        i += 1
    
if args.save_clips:
    TrainSpeakerVerificationModelAndPassword()
elif args.save_voice_password:
    TrainVoicePassword()
elif args.train_model:
    train_model()
else:
    print("You must specify either --save-clips or --save-voice-password, but not both.")
    
