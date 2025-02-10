import json, os, base64, io, torchaudio

from flask import Flask , render_template
from flask_socketio import SocketIO, emit

from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'

socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins="*")

def progress_callback(generated_tokens: int, tokens_to_generate: int):
    emit('message', {'generated': f"Generated {round((generated_tokens/tokens_to_generate) * 100, 2)}%"})

# MODELS: dict[str, MusicGen] = {}

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on("message")
def handle_generate(message):
    message = json.loads(message)
    if "op" not in message:
        print("Received a message without operation!")
        return
    
    if message["op"] == "generateMusic":
        model_name = message['model']
        emit('message', {'generated': f"Loading {model_name} model"})
        if model_name not in MODELS:
            MODELS[model_name] = MusicGen.get_pretrained(f"facebook/musicgen-{model_name}")

        model = MODELS[model_name]
        model.set_custom_progress_callback(progress_callback=progress_callback)
        model.set_generation_params(
            use_sampling=True,
            top_k=int(message["top_k"]),
            top_p=int(message["top_p"]),
            duration=int(message["duration"])
        )
        if message["audioData"]:
            try:
                audio_data = base64.b64decode(message["audioData"])
                audio_io = io.BytesIO(audio_data)
                waveform, rate = torchaudio.load(audio_io)

                wav = model.generate_with_chroma(
                    descriptions=message["prompt"],
                    melody_wavs=waveform,
                    melody_sample_rate=rate,
                    progress=True
                )
            except RuntimeError as e:
                emit('message', {'generated': e})
        else:
            wav = model.generate(
                descriptions=message["prompt"],
                progress=True
            )

        emit('message', {'generated': "Almost Done!"})
        for idx, one_wav in enumerate(wav):
            audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
            filename = f'{idx}.wav'
            
            with open(filename, 'rb') as f:
                audio_data = base64.b64encode(f.read()).decode('utf-8')
            emit('audio_data', {'audio_data': audio_data})
            os.remove(filename)

if __name__=='__main__':
    socketio.run(app, host="127.0.0.1", port=5000)