from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/data")
def data():
    conn = sqlite3.connect("emotion_data.db")
    cur = conn.cursor()
    cur.execute("SELECT emotion, COUNT(*) FROM emotion_logs GROUP BY emotion")
    rows = cur.fetchall()
    conn.close()

    return jsonify({
        "labels":[r[0] for r in rows],
        "values":[r[1] for r in rows]
    })

if __name__ == "__main__":
    app.run(debug=True)
