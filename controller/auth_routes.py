from main import app
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from controller.models import *

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'email' in session:
            flash('You are already logged in', 'info')
            return redirect(url_for('home'))
        context = {
            'role': session.get('role', 'guest'),
        }
        return render_template('login.html',context=context)
    elif request.method == 'POST':
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        
        # Here you would typically check the credentials against a database
        if not email or not password:
            flash('Email and password are required', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('login'))
        if user.password != password:
            flash('Incorrect password', 'danger')
            return redirect(url_for('login'))
        
        session['email'] = user.email
        session['role'] = user.role

        flash('Login successful', 'success')
        return redirect(url_for('home'))
    
@app.route('/logout')
def logout():
    if 'email' not in session:
        flash('You are not logged in', 'warning')
        return redirect(url_for('login'))
    session.pop('email', None)
    session.pop('role', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if 'email' in session:
            flash('You are already logged in', 'info')
            return redirect(url_for('home'))
        return render_template('register.html')
    elif request.method == 'POST':
        name = request.form.get('name', None)
        email = request.form.get('email', None)
        address = request.form.get('address', None)
        pincode = request.form.get('pincode', None)
        password = request.form.get('password', None)
        confirm_password = request.form.get('password2', None)

        if not name or not email or not password or not confirm_password:
            flash('All fields are required', 'danger')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))

        new_user = User(name=name, email=email,address=address,pincode=pincode, password=password, role='user')
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))