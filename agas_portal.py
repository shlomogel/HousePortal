from flask import Flask, render_template, jsonify
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler

app = Flask(__name__)

# Initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

sheet_id = "1aZ8NXVGa3MLiXEdTrwJ4O5OxAFq9u3qPKTTi1qgAAj4"
tasks = None


def fetch_data():
    global tasks
    tasks = pd.read_csv(
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    ).fillna("")
    print("Data refreshed")


@scheduler.task("interval", id="fetch_sheet_data", seconds=300, misfire_grace_time=900)
def scheduled_task():
    fetch_data()


fetch_data()


@app.route("/")
def hello():
    return render_template("index.html", tasks=tasks.values.tolist())


@app.route("/get_tasks/")
def get_tasks():
    return jsonify(tasks.values.tolist())


if __name__ == "__main__":
    app.run(debug=True)
