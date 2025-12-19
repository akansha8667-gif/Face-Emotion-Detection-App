from flask import Flask, render_template, request, redirect, url_for, session, flash
from login import login_user, register_user, logout_user, login_required
from emotion_detection import detect_emotion_from_image
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        flash('Username already exists')
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/detect', methods=['POST'])
@login_required
def detect():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            emotion = detect_emotion_from_image(filepath)
            return render_template('result.html', emotion=emotion, image=file.filename)
    elif 'webcam_image' in request.form:
        # Handle base64 image from webcam (processed in JS)
        import base64
        image_data = request.form['webcam_image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'webcam_capture.png')
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        emotion = detect_emotion_from_image(filepath)
        return render_template('result.html', emotion=emotion, image='webcam_capture.png')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)