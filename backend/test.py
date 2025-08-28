from TTS.api import TTS
tts = TTS(model_name="tts_models/en/ljspeech/glow-tts")
tts.tts_to_file(text="Hello there!", file_path="output.wav")
print("Success!")
