import os, csv, random
from flask import Blueprint, request, render_template, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io

handwriting_bp = Blueprint("handwriting", __name__)
LOG_FILE = "captcha_logs.csv"
PHRASES = ["human only", "no bots allowed", "stay real"]

FONT_PATH = os.path.join("static", "fonts", "cursive.ttf")  

@handwriting_bp.route('/handwriting/new')
def new_handwriting():
    phrase = random.choice(PHRASES)
    return render_template("handwriting.html", phrase=phrase)

@handwriting_bp.route('/handwriting/image')
def handwriting_image():
    phrase = request.args.get("phrase", "")
    img = Image.new("RGB", (350, 80), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 40)
    draw.text((10, 20), phrase, font=font, fill=(0, 0, 0))
    # img = img.filter(ImageFilter.GaussianBlur(radius=1))  # Less blur (was 2)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@handwriting_bp.route('/handwriting/submit', methods=['POST'])
def check_handwriting():
    user = request.form.get("answer","").strip().lower()
    correct = user == request.form.get("phrase","").strip().lower()
    log("handwriting", request.form.get("phrase"), user, correct)
    return render_template("base.html",correct=correct)

def log(t, label, choice, correct):
    header = not os.path.exists(LOG_FILE)
    with open(LOG_FILE,'a',newline='') as f:
        w=csv.writer(f)
        if header: w.writerow(["type","label","choice","correct"])
        w.writerow([t,label,choice,int(correct)])
    return render_template("base.html",correct=correct)