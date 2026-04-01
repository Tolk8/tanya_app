from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


data = load_data()


@app.route("/")
def index():
    date = request.args.get("date")

    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    clients = data.get(date, [])

    today = datetime.today()
    start = today - timedelta(days=today.weekday())
    week = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    return render_template("index.html", date=date, clients=clients, week=week)


@app.route("/add", methods=["POST"])
def add():
    global data

    date = request.form["date"]
    name = request.form["name"]
    workout = request.form["workout"]

    if date not in data:
        data[date] = []

    # ищем клиента
    client = None
    for c in data[date]:
        if c["name"] == name:
            client = c
            break

    if not client:
        client = {
            "name": name,
            "history": []
        }
        data[date].append(client)

    client["history"].append({
        "workout": workout,
        "time": datetime.now().strftime("%H:%M"),
        "done": False
    })

    save_data(data)
    return redirect(url_for("index", date=date))


@app.route("/done", methods=["POST"])
def done():
    global data

    date = request.form["date"]
    name = request.form["name"]
    index = int(request.form["index"])

    for c in data.get(date, []):
        if c["name"] == name:
            if 0 <= index < len(c["history"]):
                c["history"][index]["done"] = True

    save_data(data)
    return redirect(url_for("index", date=date))


if __name__ == "__main__":
    app.run(debug=True)
