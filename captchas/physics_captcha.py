import os,csv,random
from flask import Blueprint,request,render_template,jsonify,session

physics_bp = Blueprint("physics",__name__)
LOG_FILE="captcha_logs.csv"

@physics_bp.route("/physics/new")
def new_physics():
    target = random.randint(80,300)
    session['physics_target'] = target
    return render_template("physics.html", target=target)

@physics_bp.route("/physics/submit", methods=["POST"])
def check_physics():
    pos = float(request.form.get("pos",0))
    target = session.get('physics_target', 0)
    correct = abs(pos - target) < 20
    log("physics", target, pos, correct)
    return render_template("base.html",correct=correct)

def log(t,label,choice,correct):
    header=not os.path.exists(LOG_FILE)
    with open(LOG_FILE,"a",newline="") as f:
        w=csv.writer(f)
        if header: w.writerow(["type","label","choice","correct"])
        w.writerow([t,label,choice,int(correct)])
    return render_template("base.html",correct=correct)
