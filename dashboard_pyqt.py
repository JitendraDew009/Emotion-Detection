import sys, sqlite3, pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emotion Dashboard (PyQt)")
        self.setGeometry(300,150,800,600)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Emotion Frequency"))

        self.canvas = Canvas(Figure(figsize=(6,4)))
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.plot()

    def plot(self):
        conn = sqlite3.connect("emotion_data.db")
        df = pd.read_sql("SELECT emotion FROM emotion_logs", conn)
        conn.close()

        ax = self.canvas.figure.add_subplot(111)
        ax.clear()
        df["emotion"].value_counts().plot(kind="bar", ax=ax)
        ax.set_xlabel("Emotion")
        ax.set_ylabel("Count")
        self.canvas.draw()

app = QApplication(sys.argv)
d = Dashboard()
d.show()
sys.exit(app.exec_())
