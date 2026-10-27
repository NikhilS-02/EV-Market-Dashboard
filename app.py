import os
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()
app = Flask(__name__)

DASHBOARD_URL = os.getenv("TABLEAU_DASHBOARD_URL", "")
STORY_URL = os.getenv("TABLEAU_STORY_URL", "")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", viz_url=DASHBOARD_URL)


@app.route("/story")
def story():
    return render_template("story.html", viz_url=STORY_URL)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
