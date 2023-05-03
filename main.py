# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 22:52:48 2023

@author: Simanta Limbu
"""
from flask import Flask, render_template, url_for, redirect, request, send_from_directory,abort,flash
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from User import User, db
from Login import LoginForm
from register import RegisterForm
from StartScreen import StartScreen
from Image import ImageProcessor
from ImageModel import Image
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return StartScreen.home()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    saved_images = Image.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', saved_images=saved_images)

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():  
    final_pred = ImageProcessor.process_image(request)
    saved_image = 'static/after.jpg'
    return render_template('result.html', prediction=final_pred, saved_image=saved_image)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/save_result', methods=['POST'])
def save_result():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    image_path = request.form.get('image_path')
    result = request.form.get('result')

    ImageProcessor.save_image_result(image_path, result, current_user.id)

    return redirect(url_for('dashboard'))

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/delete_image/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    if image.user_id != current_user.id:
        abort(403)

    db.session.delete(image)
    db.session.commit()

    
    file_path = os.path.join(app.static_folder, image.file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"File not found: {file_path}")

    flash('Image has been deleted.', 'success')
    return redirect(url_for('saved_images')) 


@app.route('/saved_images')
@login_required
def saved_images():
    user_images = Image.query.filter_by(user_id=current_user.id).all()
    return render_template('saved_images.html', saved_images=user_images)

if __name__ == "__main__":
    app.run(debug=True)
