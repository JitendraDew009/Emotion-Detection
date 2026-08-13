# Emotion Detection — AI Emotion Detection System

Real-time emotion detection using a webcam and DeepFace, with optional music playback and simple dashboards for analytics (web and PyQt). Intended for demo, prototyping, and educational projects where you want to visualize detected emotions, log them to CSV/SQLite, and play mood-matching music.

## Stack
- Language(s): Python (primary), HTML (templates)
- Framework / runtime: plain Python scripts + Flask for the web dashboard; PyQt5 for the desktop UI
- Notable libraries: deepface (emotion analysis), OpenCV (cv2) for capture & face detection, PyQt5 for the UI, pygame for audio playback, Flask for the web dashboard, pandas & matplotlib for the PyQt dashboard

## What’s included / How it’s organized
Top-level files and directories:
- main.py            — Desktop application (PyQt) that captures webcam frames, detects faces, analyzes emotion with DeepFace, logs to CSV/SQLite, and plays music based on emotion.
- dashboard_web.py   — Flask web dashboard that serves a template and returns emotion counts from the SQLite DB as JSON.
- dashboard_pyqt.py  — Simple PyQt window that plots emotion counts from the SQLite DB using matplotlib.
- templates/         — HTML templates for the Flask dashboard.
  - templates/dashboard.html — Web dashboard page (uses Chart.js).
- emotion_data.db    — SQLite database used by the app (emotion_logs table).
- emotion_log.csv    — CSV log of detected emotions (appends new rows).
- music/              — (not included) expected folder containing .mp3 files referenced by the app.

How it fits together:
- main.py is the runtime: it reads frames from the webcam, uses OpenCV Haar cascades to find faces, and runs DeepFace.analyze (actions=["emotion"]) periodically (every N frames). Detected emotions and confidences are logged to emotion_data.db and emotion_log.csv and trigger playback of matching music via pygame.
- dashboard_web.py queries emotion_data.db (GROUP BY emotion) and provides JSON for templates/dashboard.html, which renders a Chart.js bar chart.
- dashboard_pyqt.py reads emotion_data.db into a pandas DataFrame and draws a bar chart inside a PyQt window.

## Features
- Real-time webcam emotion analysis (DeepFace).
- Plays music mapped to detected emotions (configurable).
- Logs each detection to both SQLite (emotion_logs table) and CSV.
- Two dashboards:
  - Web dashboard (Flask + Chart.js)
  - Desktop dashboard (PyQt + matplotlib)

## Requirements
Core Python packages used in the repository:
- deepface
- opencv-python
- PyQt5
- pygame
- Flask
- pandas
- matplotlib
- sqlite3 (standard library)
DeepFace requires a deep learning backend (TensorFlow). On many systems you should install tensorflow or tensorflow-cpu.

Example minimal requirements (save as requirements.txt if you want):
deepface
opencv-python
PyQt5
pygame
Flask
pandas
matplotlib
tensorflow    # or tensorflow-cpu

## Quick setup (recommended)
1. Create and activate a virtual environment:
   - python -m venv .venv
   - source .venv/bin/activate   (Linux / macOS)
   - .venv\Scripts\activate      (Windows)

2. Install dependencies:
   - pip install -r requirements.txt
   - or:
     pip install deepface opencv-python PyQt5 pygame Flask pandas matplotlib tensorflow

3. Prepare music files:
   - Create a directory named `music/` in the project root.
   - Place MP3 files named (or update names in main.py):
     - happy.mp3
     - sad.mp3
     - angry.mp3
     - neutral.mp3
   - You can change the mapping in main.py: the `emotion_music` dict maps emotion -> filename.

## How to run

Run the desktop emotion detector (main app):
- python main.py
  - This opens the PyQt window, accesses your default webcam (cv2.VideoCapture(0)), analyzes emotion every DETECT_EVERY_N_FRAMES frames (default 10), logs data, and plays music via pygame.

Run the web dashboard:
- python dashboard_web.py
  - Then open http://127.0.0.1:5000/ to see the Chart.js visualization. The endpoint /data returns emotion counts from `emotion_data.db`.

Run the PyQt dashboard:
- python dashboard_pyqt.py

Notes:
- The app writes/reads `emotion_data.db` in the project root. If the file does not exist, main.py creates the table.
- The app also writes/updates `emotion_log.csv` (first-run header is created if file is empty).
- If your webcam is at a different index, change cv2.VideoCapture(0) in main.py to another index (1, 2, ...).

## Configuration (quick reference)
- DETECT_EVERY_N_FRAMES (main.py) — how often (in frames) to run DeepFace.analyze (default 10).
- MUSIC_PATH (main.py) — relative path to music files (default "music/").
- emotion_music (main.py) — dict mapping emotion names to mp3 filenames.
- APP_MODE, SESSION_ID — metadata fields stored with logs.

## Data schema (emotion_logs table)
Columns:
- id, date, time, face_id, emotion, confidence, fps, music, session_id, app_mode

## Troubleshooting & tips
- DeepFace may require a working TensorFlow installation; if you see import or model errors, install tensorflow or tensorflow-cpu.
- If no faces are detected: ensure proper lighting and that the webcam is working. Try increasing contrast or moving the camera.
- If audio doesn't play: ensure pygame can access your OS audio drivers; test with a simple pygame audio script.
- If CPU/GPU is slow: DeepFace runs heavy models — consider switching to lighter backends/models or reduce analysis frequency (increase DETECT_EVERY_N_FRAMES).
- To disable music playback for testing, comment out calls to play_music in analyze_emotion or remove pygame initialization.

## Security & privacy
- This project captures webcam frames and writes logs locally to CSV and SQLite. Use responsibly and ensure you have permission to capture video from others.
- Do not upload or expose `emotion_data.db` or `emotion_log.csv` publicly if they contain sensitive data.

## Extending the project
- Add more emotion→music mappings or use online streaming audio.
- Add authentication and filters to the Flask dashboard.
- Store more detailed per-face tracking (multiple face IDs).
- Replace the Haar cascade with a more robust face detector (MTCNN, dlib, or RetinaFace) for better reliability.

## Contributing
Contributions are welcome. Open an issue or submit a pull request with:
- A short description of the change
- Why it’s needed
- Tests or usage notes where appropriate

## License
No license file is included in this repository. 

## Contact
LinkedIn or GMail 
