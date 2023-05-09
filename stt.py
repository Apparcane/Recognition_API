import vosk
import json
import wave

# Initialize Recognite
model = vosk.Model("model_small")
vosk.SetLogLevel(-1)
samplerate = 16000
rec = vosk.KaldiRecognizer(model, samplerate)

#Enter Sound File
def recognite(file):
    file = wave.open(file, "rb")
    data = file.readframes(file.getnframes())
    
    #Recognition
    rec.AcceptWaveform(data)
    result = json.loads(rec.FinalResult())
    
    return result['text']
    

