from flask import Flask, redirect, url_for, render_template, request, session, flash
import random
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

from captchas.physics_captcha import physics_bp
from captchas.logic_story_captcha import logic_story_bp
from captchas.emotion_captcha import emotion_bp
from captchas.handwriting_captcha import handwriting_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",         # your MySQL username
    password="JR@15092005", # your MySQL password
    database="captcha_db"
)
cursor = db.cursor(dictionary=True)

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
    if 'user_id' in session:
        captcha_route = random.choice(CAPTCHA_ROUTES)
        return redirect(url_for(captcha_route))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                           (username, email, password))
            db.commit()
            flash('Signup successful! Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error:
            flash('Username or email already exists.', 'danger')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/base')
def base():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)