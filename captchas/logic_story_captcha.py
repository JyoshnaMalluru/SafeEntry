import os,csv,random
from flask import Blueprint, redirect,request,render_template,jsonify, url_for

logic_story_bp = Blueprint("logic_story",__name__)
LOG_FILE="captcha_logs.csv"
STORIES=[
    ("story1.png", "Who will die at the end?", "lion"),
    ("story2.jpeg", "What did crow use to drink water in vessel?", "stones"),
]

@logic_story_bp.route("/logic_story/new")
def new_story():
    image, question, answer = random.choice(STORIES)
    return render_template("logic_story.html", image=image, question=question, answer=answer)

@logic_story_bp.route("/logic_story/submit", methods=["POST"])
def check_story():
    ans = request.form.get("answer", "").strip().lower()
    correct = ans == request.form.get("correct", "").strip().lower()
    log("logic_story", request.form.get("correct"), ans, correct)
    return redirect(url_for("base", correct=int(correct)))

def log(t, label, choice, correct):
    header = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        w = csv.writer(f)
        if header: w.writerow(["type", "label", "choice", "correct"])
        w.writerow([t, label, choice, int(correct)])
    return render_template("base.html",correct=correct)
