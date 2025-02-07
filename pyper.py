from piper.voice import PiperVoice as piper #Backbone of text to speech
import wave #Writing text to speech to wave files
from sys import platform
from os import remove
from os import environ
from playsound import playsound

# Check if the operating system is MacOS
if platform == 'darwin':
    print('This library cannot be used on MacOS yet, due to piper not being supported there.')
    exit() # Piper isn't available on MacOS yet

class Pyper:
    def __init__(self, model):
        self.model = None
        self.voice = None

        if '.onnx' in model: # Is the extension .onnx in the filename, if not add it below.
            self.model = model # Set model variable as is.
        else:
            self.model = model + '.onnx' # Set model variable and append .onnx.
        
        # Try to load the model
        try:
            self.voice = piper.load(model) # Load the model
        except:
            print("Something went wrong, did you type the correct name for the model?")
            exit()

    # Function to save a text to speech file to disk
    def save(self, text, file_name):
            with wave.open(file_name, "wb") as wav_file:
                self.voice.synthesize(text, wav_file)

    # Function to save the file to disk, play it on the speakers, then delete the file.
    def say(self, text):
        self.save(text, 'tmp_text_2_speech.wav', self.model) # Save the text to speech file to disk
        
        # Play the audio file
        playsound('tmp_text_2_speech.wav')
        
        remove("tmp_text_2_speech.wav") # Remove the temporary file