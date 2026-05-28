from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL
import librosa
import numpy as np
import soundfile as sf
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

os.makedirs("audio", exist_ok=True)
os.makedirs("output", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    enhanced_ready = False
    
    if request.method == "POST":
        youtube_url = request.form["youtube_url"]
        
        # Download audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            'outtmpl': 'audio/input',
            'quiet': True
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        
        # AI Enhancement using Librosa
        y, sr = librosa.load("audio/input.wav")
        
        # Noise reduction using spectral subtraction
        S = librosa.stft(y)
        S_mag = np.abs(S)
        S_phase = np.angle(S)
        
        # Subtract noise from first 0.5 seconds
        noise = np.mean(S_mag[:, :int(0.5*sr/512)], axis=1, keepdims=True)
        S_mag_reduced = np.maximum(S_mag - 2*noise, 0)
        
        S_enhanced = S_mag_reduced * np.exp(1j * S_phase)
        y_enhanced = librosa.istft(S_enhanced)
        
        sf.write("output/input_enhanced.wav", y_enhanced, sr)
        
        enhanced_ready = True
    
    return render_template(
        "index.html",
        enhanced_ready=enhanced_ready
    )

@app.route("/download")
def download():
    return send_file(
        "output/input_enhanced.wav",
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)