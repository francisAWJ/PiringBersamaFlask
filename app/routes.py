from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, DonateForm
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy as sa
from app.models import User, Donation

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Welcome to Piring Bersama')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        
        if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
        
        login_user(user)
        next_page = request.args.get('next')
        
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/donasi_saya')
@login_required
def donasi_saya():
    donations = db.session.scalars(sa.select(Donation).where(Donation.user_id == current_user.id))
    return render_template('donasi_saya.html', title='Donasi Saya', donations=donations)

@app.route('/donasi', methods=['GET', 'POST'])
@login_required
def donasi():    
    form = DonateForm()

    if form.validate_on_submit():
        donation = Donation(
            address=form.address.data,
            phone_number=form.phone_number.data,
            food_type=form.food_type.data,
            portions=form.portions.data,
            food_desc=form.food_desc.data,
            author=current_user
        )
        db.session.add(donation)
        db.session.commit()
        flash('Terima kasih atas donasi anda!')
        return redirect(url_for('donasi_saya'))

    return render_template('donasi.html', title='Buat Donasi', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
     if current_user.is_authenticated:
        return redirect(url_for('index'))
     
     form = RegistrationForm()

     if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            first_name=form.first_name.data, 
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Selamat! Anda telah terdaftar dengan kami!')
        return redirect(url_for('login'))
     
     return render_template('register.html', title='Daftar', form=form)

@app.route('/kelompok_kami')
def kelompok_kami():
    return render_template('kelompok.html', title='Kelompok Kami')
        