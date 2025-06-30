from main import app
from flask import render_template, request, redirect, url_for, flash, session
from controller.models import *
from datetime import datetime

@app.route('/')
def home():
    user_email = session.get('email', None)
    user_name = None
    if user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            user_name = user.name
    lots = ParkingLot.query.all()
    context = {
        'title': 'Home',
        'message': 'Welcome to the Vehicle Parking App',
        'name': user_name,
        'lots': lots
    }
    return render_template('home.html', context=context)

@app.route('/users', methods=['GET'])
def users():
    users = User.query.filter_by(role='user').all()
    context = {
        'title': 'Users',
        'users': users
    }
    return render_template('users.html', context=context)

@app.route('/add_parking_lot', methods=['GET', 'POST'])
def add_parking_lot():
    if 'role' not in session or session['role'] != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form.get('lotname')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        price = request.form.get('price')
        capacity = int(request.form.get('maxspots'))  # Ensure it's an integer

        # Create the parking lot
        new_lot = ParkingLot(
            name=name,
            address=address,
            pincode=pincode,
            price_per_hour=price,
            max_spots=capacity
        )
        db.session.add(new_lot)
        db.session.commit()  # Commit to get the new_lot.id

        # Create parking spots for this lot
        for i in range(1, capacity + 1):
            spot = ParkingSpot(
                lot_id=new_lot.id,
                status='A'  # Available
            )
            db.session.add(spot)
        db.session.commit()

        flash('Parking lot and spots added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_parking_lot.html', title='Add Parking Lot')

@app.route('/parking_lots', methods=['GET'])
def parking_lots():
    lots = ParkingLot.query.all()
    context = {
        'title': 'Parking Lots',
        'lots': lots
    }
    return render_template('parking_lot.html', context=context)

@app.route('/edit_parking_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    if request.method == 'POST':
        lot.name = request.form['lotname']
        lot.address = request.form['address']
        lot.pincode = request.form['pincode']
        lot.price_per_hour = request.form['price']
        CurrentSpots = int(lot.max_spots)
        lot.max_spots = int(request.form['maxspots'])
        if lot.max_spots < CurrentSpots:
            for spot in lot.spots[lot.max_spots:]:
                if spot.status == 'A':
                    db.session.delete(spot)
        elif lot.max_spots > CurrentSpots:
            for i in range(CurrentSpots + 1, lot.max_spots + 1):
                new_spot = ParkingSpot(lot_id=lot.id, status='A')
                db.session.add(new_spot)
        # Commit changes to the database    
        db.session.commit()
        flash('Parking lot updated!', 'success')
        return redirect(url_for('home'))
    return render_template('home.html', lot=lot)

@app.route('/delete_parking_lot/<int:lot_id>', methods=['POST'])
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    db.session.delete(lot)
    db.session.commit()
    flash('Parking lot deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/delete_parking_spot/<int:spot_id>', methods=['POST'])
def delete_parking_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.status != 'A':  # Only allow deletion of available spots
        flash('Only available parking spots can be deleted.', 'danger')
        return redirect(request.referrer or url_for('parking_lots'))
    db.session.delete(spot)
    lot = ParkingLot.query.get(spot.lot_id)
    lot.max_spots -= 1  # Decrease the max spots count
    db.session.commit()
    flash('Parking spot deleted!', 'success')
    return redirect(request.referrer or url_for('parking_lots'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        lots = ParkingLot.query.filter(
            (ParkingLot.name.ilike(f'%{query}%')) |
            (ParkingLot.address.ilike(f'%{query}%')) |
            (ParkingLot.pincode.ilike(f'%{query}%'))
        ).all()
        return render_template('search.html', context=lots, query=query)
    else:
        # If GET request, just render the search page without results
        return render_template('search.html', context='Search Parking Lots')
    
@app.route('/summary', methods=['GET'])
def summary():
    if 'role' not in session or session['role'] != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    
    total_users = User.query.count()
    total_parking_lots = ParkingLot.query.count()
    total_reservations = Reservation.query.count()
    lots = ParkingLot.query.all()
    context = {
        'title': 'Summary',
        'lots': lots
    }
    
    return render_template('summary.html', context=context)