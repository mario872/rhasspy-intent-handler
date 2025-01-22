import logging
import warnings
logging.disable(logging.CRITICAL)
warnings.simplefilter(action='ignore', category=FutureWarning)

import torch
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.audio import Audio
from pyannote.core import Segment
from scipy.spatial.distance import cdist
import speech_recognition as sr

# Initialize the speaker embedding model
model = PretrainedSpeakerEmbedding(
    "speechbrain/spkrec-ecapa-voxceleb",
    device=torch.device("cpu")
)
audio_processor = Audio(sample_rate=16000, mono="downmix")

def get_embedding(audio_file, start_time, end_time):
    """
    Extract embedding for a specific time segment of an audio file.
    """
    waveform, sample_rate = audio_processor(audio_file)
    return model(waveform[None])

def compute_average_embedding(audio_files, start_time, end_time):
    """
    Compute the average embedding from multiple audio files.
    """
    embeddings = []
    for audio_file in audio_files:
        embedding = get_embedding(audio_file, start_time, end_time)
        # Convert numpy.ndarray to torch.Tensor
        embeddings.append(torch.tensor(embedding))
    return torch.mean(torch.stack(embeddings), dim=0)

def is_your_voice(reference_embedding, test_audio_file, test_start, test_end, threshold=0.4):
    """
    Compare the speaker in a test audio segment to a reference embedding.
    """
    test_embedding = get_embedding(test_audio_file, test_start, test_end)
    distance = cdist(reference_embedding, test_embedding, metric="cosine")[0][0]
    return distance < threshold

def transcribe_audio(audio_file, reference_embedding, start_time, end_time):
    """
    Perform speech-to-text if the voice matches the reference embedding.
    """
    if not is_your_voice(reference_embedding, audio_file, start_time, end_time):
        print("Voice not recognized as yours.")
        return None

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)  # Replace with preferred STT method
    except sr.UnknownValueError:
        print("Could not understand the audio.")
    except sr.RequestError as e:
        print(f"Request error: {e}")
    return None

# Example Usage
if __name__ == "__main__":
    # List of audio files with your voice
    reference_audio_files = ["audio1.wav", "audio2.wav", "audio3.wav"]

    # Generate the average embedding from multiple recordings
    ref_embedding = compute_average_embedding(reference_audio_files, start_time=0, end_time=5)  # Adjust times

    # Test with another audio file
    test_audio = "test_audio.wav"
    result = transcribe_audio(test_audio, ref_embedding, start_time=0, end_time=5)  # Adjust times
    if result:
        print(f"Transcription: {result}")
