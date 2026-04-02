from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"


# 📥 загрузка данных
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


# 💾 сохранение данных
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


data = load_data()


# 🏠 главная страница
@app.route("/")
def index():
    date = request.args.get("date")

    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    clients = data.get(date, [])

    today = datetime.today()
    start = today - timedelta(days=today.weekday())

    week = []
    for i in range(7):
        day = start + timedelta(days=i)
        week.append(day.strftime("%Y-%m-%d"))

    return render_template("index.html", date=date, clients=clients, week=week)


# ➕ добавление клиента
@app.route("/add", methods=["POST"])
def add():
    date = request.form["date"]
    name = request.form["name"]
    workout = request.form["workout"]

    if date not in data:
        data[date] = []

    data[date].append({
        "name": name,
        "workout": workout,
        "done": False
    })

    save_data()
    return redirect(url_for("index", date=date))


# ✅ отметить выполнено
@app.route("/done", methods=["POST"])
def done():
    date = request.form["date"]
    index = int(request.form["index"])

    if date in data and 0 <= index < len(data[date]):
        data[date][index]["done"] = True

    save_data()
    return redirect(url_for("index", date=date))


# 🚀 запуск (ВАЖНО ДЛЯ RENDER)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
