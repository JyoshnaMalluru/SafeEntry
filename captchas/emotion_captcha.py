import os,csv,random
from flask import Blueprint,request,render_template,jsonify

emotion_bp = Blueprint("emotion",__name__)
LOG_FILE="captcha_logs.csv"
EMOTIONS=[("happy.png","happy"),("sad.png","sad"),("angry.webp","angry")]

@emotion_bp.route("/emotion/new")
def new_emotion():
    img,label=random.choice(EMOTIONS)
    return render_template("emotion.html", image=img, label=label)

@emotion_bp.route("/emotion/submit", methods=["POST"])
def check_emotion():
    ans=request.form.get("answer","").strip().lower()
    label=request.form.get("label","").strip().lower()
    correct = ans==label
    log("emotion",label,ans,correct)
    return render_template("base.html",correct=correct)

def log(t,label,choice,correct):
    header=not os.path.exists(LOG_FILE)
    with open(LOG_FILE,"a",newline="") as f:
        w=csv.writer(f)
        if header: w.writerow(["type","label","choice","correct"])
        w.writerow([t,label,choice,int(correct)])
    return render_template("base.html",correct=correct)


