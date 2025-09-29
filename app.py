from flask import Flask, redirect, url_for, render_template
import random
from captchas.physics_captcha import physics_bp
from captchas.logic_story_captcha import logic_story_bp
from captchas.emotion_captcha import emotion_bp
from captchas.handwriting_captcha import handwriting_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Register blueprints
app.register_blueprint(physics_bp)
app.register_blueprint(logic_story_bp)
app.register_blueprint(emotion_bp)
app.register_blueprint(handwriting_bp)

CAPTCHA_ROUTES = [
    'physics.new_physics',
    'logic_story.new_story',
    'emotion.new_emotion',
    'handwriting.new_handwriting'
]

@app.route('/')
def home():
    captcha_route = random.choice(CAPTCHA_ROUTES)
    return redirect(url_for(captcha_route))

@app.route('/base')
def base():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)