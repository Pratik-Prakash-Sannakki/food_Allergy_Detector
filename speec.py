import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import whisper

model = whisper.load_model("large")
text = model.transcribe("recording1.wav")
# Printing the transcribed text
print(text['text'])