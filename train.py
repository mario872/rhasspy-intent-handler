from functions.secrets import voice_password
from functions import SaveVoiceClip
from notifypy import Notify
import time
from num2words import num2words
import argparse

parser = argparse.ArgumentParser(description='Train the voice password and speaker verification model.')
parser.add_argument('--train-model', action='store_true', help='Train the voice password and speaker verification model.')
parser.add_argument('--voice-password', action='store_true', help='Train the voice password.')
args = parser.parse_args()

def TrainVoicePassword():
    print("Make sure to specify your voice_password in the functions/secrets.py file.")
    for _ in range(5):
        print(voice_password + "\nPress ENTER to start recording.")
        input()
        SaveVoiceClip(location="voice_input/", index=_)

def TrainSpeakerVerificationModelAndPassword():
    TrainVoicePassword()
    
    sentences = ["This is my name and it is totally my name.", "I am totally the person I say I am.", "A bear is only dangerous in the winter because that is when it is hibernating.", "Rabbits are scary."]
    print(f"You will say {num2words(len(sentences))} different sentences, and your voice password five times.")
    i = 5
    for sentence in sentences:
        print(sentence + "\nPress ENTER to start recording.")
        input()
        SaveVoiceClip(location="voice_input/", index=i)
        i += 1
    
if args.train_model:
    TrainSpeakerVerificationModelAndPassword()
elif args.voice_password:
    TrainVoicePassword()
else:
    print("You must specify either --train-model or --voice-password, but not both.")
    
