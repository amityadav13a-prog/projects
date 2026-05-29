# 🎵 AI YouTube Audio Enhancer

An AI-powered web application that improves noisy and low-quality YouTube audio using Python-based audio processing techniques.

---

## 🚀 Features

* 🎧 Download audio directly from YouTube
* 🤖 AI-inspired audio enhancement pipeline
* 🌐 Full-stack Flask web application
* 🎨 Responsive and modern UI
* 📥 Download enhanced audio output
* 🔊 Noise reduction using spectral subtraction
* ⚡ Fast and lightweight workflow
* 📂 Organized project structure
* ❌ Invalid URL handling
* 💻 Beginner-friendly implementation

---

## 🛠 Tech Stack

### Frontend

* HTML5
* CSS3

### Backend

* Python
* Flask

### Audio Processing / AI

* Librosa
* NumPy
* SoundFile
* yt-dlp
* FFmpeg

---

## 📂 Project Structure

```txt
projects/
│
├── app.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── audio/
│
├── output/
│
├── requirements.txt
│
└── README.md
```

---

## ⚙ Installation

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/projects.git
```

---

### 2. Install Dependencies


pip install -r requirements.txt


---

### 3. Install FFmpeg

Download FFmpeg:

https://ffmpeg.org/download.html

Add FFmpeg to system PATH.

---

## ▶ Run Project

```bash
python app.py
```

Open browser:


http://127.0.0.1:5000


---

## 🧠 How It Works

1. User enters a YouTube video URL
2. Audio is downloaded using yt-dlp
3. Librosa loads and processes the audio
4. Spectral subtraction reduces background noise
5. Enhanced audio is generated
6. User downloads the improved audio

---

## 🔬 Audio Enhancement Technique

This project uses spectral subtraction for noise reduction.

### Processing Steps

* Audio is converted into frequency domain using STFT
* Noise profile is estimated from the initial audio segment
* Noise frequencies are subtracted
* Audio is reconstructed using inverse STFT

This improves speech clarity and reduces unwanted noise.

---

## 🎨 UI/UX Highlights

* Responsive design
* Dark-themed interface
* Interactive buttons
* Clean layout
* User-friendly workflow

---

## 📈 Future Improvements

* Real-time waveform visualization
* Deep learning enhancement models
* Drag-and-drop audio upload
* Audio comparison player
* Cloud deployment support
* Live microphone enhancement

---

## 📚 Learning Outcomes

Through this project I learned:

* Flask backend development
* Frontend-backend integration
* Audio signal processing
* Noise reduction techniques
* Git & GitHub workflow
* Responsive UI design
* File handling in Python

---

## 💡 Challenges Faced

* Integrating YouTube audio downloading
* Managing audio file conversions
* Implementing spectral subtraction
* Handling audio processing efficiently
* Configuring FFmpeg dependencies

---

## 👨‍💻 Author

### Amit Yadav

Passionate about:

* Software Development
* AI & ML
* Web Development
* Problem Solving
