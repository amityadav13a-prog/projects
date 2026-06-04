from flask import Flask, render_template, request, send_file, redirect, url_for
from yt_dlp import YoutubeDL
import librosa
import numpy as np
import soundfile as sf
import subprocess
import os
import time

app = Flask(__name__, static_folder='static', static_url_path='/static')

os.makedirs("downloads", exist_ok=True)
os.makedirs("audio", exist_ok=True)
os.makedirs("output", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    enhanced_ready = False
    error_message = None
    unique_id = None
    
    if request.method == "POST":
        youtube_url = request.form["youtube_url"].strip()
        
        unique_id = str(int(time.time()))
        
        if not youtube_url:
            error_message = "❌ Please enter a YouTube URL!"
            return render_template("index.html", enhanced_ready=False, error_message=error_message)
        
        if "youtube.com" not in youtube_url and "youtu.be" not in youtube_url:
            error_message = "❌ Invalid link! Please enter a valid YouTube URL."
            return render_template("index.html", enhanced_ready=False, error_message=error_message)
        
        try:
            #  Download video
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': f'downloads/{unique_id}',
                'quiet': False,
                'no_warnings': False,
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                video_file = ydl.prepare_filename(info)
            
            # Extract audio
            audio_file = f'audio/input_{unique_id}.wav'
            extract_cmd = [
                "ffmpeg",
                "-i", video_file,
                "-vn",
                "-acodec", "pcm_s16le",
                "-ar", "44100",
                "-ac", "2",
                audio_file,
                "-y"
            ]
            
            result = subprocess.run(extract_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                error_message = "❌ Error extracting audio. FFmpeg error."
                return render_template("index.html", enhanced_ready=False, error_message=error_message)
            
            #  AI Enhancement
            y, sr = librosa.load(audio_file, sr=44100)

            # Normalize input
            y = y / np.max(np.abs(y))

            # STFT
            S = librosa.stft(y)
            S_mag = np.abs(S)
            S_phase = np.angle(S)

            # Stronger noise reduction
            noise = np.mean(S_mag[:, :int(0.5*sr/512)], axis=1, keepdims=True)
            S_mag_reduced = np.maximum(S_mag - 4*noise, 0)

            # Soft thresholding for better quality
            threshold = np.percentile(S_mag_reduced, 5)
            S_mag_reduced[S_mag_reduced < threshold] = 0

            S_enhanced = S_mag_reduced * np.exp(1j * S_phase)
            y_enhanced = librosa.istft(S_enhanced)

            # Normalize और volume boost करो
            y_enhanced = y_enhanced / np.max(np.abs(y_enhanced))
            y_enhanced = y_enhanced * 1.2

            # Clip to prevent distortion
            y_enhanced = np.clip(y_enhanced, -1, 1)

            enhanced_audio = f'audio/enhanced_{unique_id}.wav'
            sf.write(enhanced_audio, y_enhanced, sr)
            
            # Step 4: Merge video with enhanced audio
            output_file = f'output/enhanced_{unique_id}.mp4'
            merge_cmd = [
                "ffmpeg",
                "-i", video_file,
                "-i", enhanced_audio,
                "-c:v", "copy",
                "-c:a", "aac",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                output_file,
                "-y"
            ]
            
            result = subprocess.run(merge_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                error_message = "❌ Error merging video and audio."
                return render_template("index.html", enhanced_ready=False, error_message=error_message)
            
            enhanced_ready = True
            
            return render_template("index.html", enhanced_ready=enhanced_ready, error_message=error_message, unique_id=unique_id)
            
        except Exception as e:
            error_message = f"❌ Error: {str(e)[:100]}"
            return render_template("index.html", enhanced_ready=False, error_message=error_message)
    
    return render_template("index.html", enhanced_ready=enhanced_ready, error_message=error_message, unique_id=unique_id)

@app.route("/download/<unique_id>")
def download(unique_id):
    try:
        return send_file(
            f"output/enhanced_{unique_id}.mp4",
            as_attachment=True,
            download_name="enhanced_video.mp4"
        )
    except Exception as e:
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)