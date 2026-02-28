from tortoise.api import TextToSpeech
# from tortoise.utils.audio import save_wav
import soundfile as sf

# Initialize the TTS engine
tts = TextToSpeech()

# Define the text you want to convert to speech
text = "Hello, this is an example of Tortoise TTS. How are you?"

# Generate speech (audio waveform) from the text
voice = "standard"  # Choose a voice model; Tortoise has several pre-trained models
wav = tts.text_to_speech(text, voice)

# Save the audio to a file
# save_wav("output.wav", wav)
sf.write("output.wav", wav, samplerate=22050)

print("Audio saved as output.wav")