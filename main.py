import sys, cv2, time, csv, threading, uuid, sqlite3
from datetime import datetime
from deepface import DeepFace
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import pygame

DETECT_EVERY_N_FRAMES = 10
CSV_FILE = "emotion_log.csv"
DB_FILE = "emotion_data.db"
MUSIC_PATH = "music/"
SESSION_ID = str(uuid.uuid4())[:8]
APP_MODE = "Desktop-Windows"

last_emotion = "Detecting"
last_confidence = 0.0
frame_count = 0
current_music = None
prev_time = time.time()
fps = 0

pygame.mixer.init()

emotion_music = {
    "happy": "happy.mp3",
    "sad": "sad.mp3",
    "angry": "angry.mp3",
    "neutral": "neutral.mp3"
}

# ---------- DATABASE ----------
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS emotion_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    time TEXT,
    face_id TEXT,
    emotion TEXT,
    confidence REAL,
    fps INTEGER,
    music TEXT,
    session_id TEXT,
    app_mode TEXT
)
""")
conn.commit()

# ---------- CSV ----------
with open(CSV_FILE, "a", newline="") as f:
    if f.tell() == 0:
        csv.writer(f).writerow([
            "Date","Time","Face_ID","Emotion",
            "Confidence(%)","FPS","Music",
            "Session_ID","App_Mode"
        ])

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

def play_music(emotion):
    global current_music
    if emotion in emotion_music:
        song = emotion_music[emotion]
        if current_music != song:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(MUSIC_PATH + song)
            pygame.mixer.music.play(-1)
            current_music = song

def save_data(face_id, emotion, confidence, fps, music):
    date = str(datetime.now().date())
    time_now = time.strftime("%H:%M:%S")

    cursor.execute("""
    INSERT INTO emotion_logs
    (date,time,face_id,emotion,confidence,fps,music,session_id,app_mode)
    VALUES (?,?,?,?,?,?,?,?,?)
    """, (date, time_now, face_id, emotion, confidence, fps, music, SESSION_ID, APP_MODE))
    conn.commit()

    with open(CSV_FILE, "a", newline="") as f:
        csv.writer(f).writerow([
            date, time_now, face_id, emotion,
            confidence, fps, music, SESSION_ID, APP_MODE
        ])

def analyze_emotion(face):
    global last_emotion, last_confidence
    try:
        result = DeepFace.analyze(face, actions=["emotion"], enforce_detection=False)
        emotions = result[0]["emotion"]
        last_emotion = max(emotions, key=emotions.get)
        last_confidence = round(emotions[last_emotion], 2)

        play_music(last_emotion)
        save_data("Face-1", last_emotion, last_confidence, fps,
                  emotion_music.get(last_emotion, "None"))
    except:
        pass

class EmotionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Emotion Detection System")
        self.setGeometry(200, 100, 900, 650)

        self.image = QLabel()
        self.status = QLabel("Emotion: Detecting")
        self.exit_btn = QPushButton("Exit")
        self.exit_btn.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.image)
        layout.addWidget(self.status)
        layout.addWidget(self.exit_btn)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)

    def update_frame(self):
        global frame_count, prev_time, fps
        ret, frame = cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        curr_time = time.time()
        fps = int(1 / (curr_time - prev_time)) if curr_time != prev_time else fps
        prev_time = curr_time

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x,y,w,h) in faces:
            face = frame[y:y+h, x:x+w]
            if frame_count % DETECT_EVERY_N_FRAMES == 0:
                threading.Thread(target=analyze_emotion, args=(face,), daemon=True).start()

            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(frame,f"{last_emotion} ({last_confidence}%)",
                        (x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)

        frame_count += 1
        self.status.setText(f"Emotion: {last_emotion} ({last_confidence}%) | FPS: {fps}")

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h,w,ch = rgb.shape
        img = QImage(rgb.data,w,h,ch*w,QImage.Format_RGB888)
        self.image.setPixmap(QPixmap.fromImage(img))

    def closeEvent(self,event):
        cap.release()
        pygame.mixer.music.stop()
        conn.close()
        event.accept()

app = QApplication(sys.argv)
window = EmotionApp()
window.show()
sys.exit(app.exec_())
