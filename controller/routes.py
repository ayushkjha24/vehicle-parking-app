from main import app
from flask import render_template, request, redirect, url_for, flash, session
from controller.models import *
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

@app.route('/')
def home():
    user_email = session.get('email', None)
    lots = ParkingLot.query.all()
    user_name = None
    reservations = None
    if user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            user_name = user.name
            reservations = Reservation.query.filter_by(user_id=user.id).order_by(Reservation.start_time.desc()).all() 
    Reservations = Reservation.query.all()
    dateTime = datetime.now().strftime("%Y-%m-%d %H:%M")
    context = {
        'title': 'Home',
        'message': 'Welcome to the Vehicle Parking App',
        'name': user_name,
        'lots': lots,
        'reservations': reservations,
        'Reservations': Reservations,
        'dateTime': dateTime,
    }
    return render_template('home.html', context=context)

@app.route('/users', methods=['GET'])
def users():
    if 'role' not in session or session['role'] != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
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
    if 'role' not in session or session['role'] != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    # Fetch all parking lots from the database  
    lots = ParkingLot.query.all()
    context = {
        'title': 'Parking Lots',
        'lots': lots
    }
    return render_template('parking_lot.html', context=context)

@app.route('/edit_parking_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_parking_lot(lot_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
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
    if 'role' not in session or session['role'] != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    lot = ParkingLot.query.get_or_404(lot_id)
    if lot.occupied_spots() == 0:
        db.session.delete(lot)
        db.session.commit()
        flash('Parking lot deleted!', 'success')
    else:
        flash('You can\'t delete this lot, Some spots are being used','danger')
    return redirect(url_for('home'))

@app.route('/delete_parking_spot/<int:spot_id>', methods=['POST'])
def delete_parking_spot(spot_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.status == 'A':  # Only allow deletion of available spots    
        db.session.delete(spot)
    else:
        flash('Only available parking spots can be deleted.', 'danger')
        return redirect(request.referrer or url_for('parking_lots'))
    lot = ParkingLot.query.get(spot.lot_id)
    lot.max_spots -= 1  # Decrease the max spots count
    db.session.commit()
    flash('Parking spot deleted!', 'success')
    return redirect(request.referrer or url_for('parking_lots'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        location = request.form.get('location')
        pincode = request.form.get('pincode')
        lots = ParkingLot.query.filter(
            (ParkingLot.address.ilike(f'%{location}%')) |
            (ParkingLot.pincode.ilike(f'%{pincode}%'))
        ).all()
        context = {
            'title': 'Search Results',
            'lots': lots,
        }
        return render_template('search.html', context=context)
    else:
        # If GET request, just render the search page without results
        return render_template('search.html', context={'title': 'Search Parking Lots', 'lots': []})
    
@app.route('/summary', methods=['GET'])
def summary():
    if 'role' not in session or session['role'] != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    
    total_users = User.query.count()
    total_parking_lots = ParkingLot.query.count()
    total_reservations = Reservation.query.count()
    lots = ParkingLot.query.all()

    lot_names = [lot.name for lot in lots]
    available_spots = [lot.available_spots() for lot in lots]
    occupied_spots = [lot.occupied_spots() for lot in lots]

    # Stacked bar chart
    import numpy as np
    x = np.arange(len(lots))
    width = 0.5

    plt.figure(figsize=(10, 6))
    plt.bar(x, available_spots, width, label='Available', color='green')
    plt.bar(x, occupied_spots, width, bottom=available_spots, label='Occupied', color='red')
    plt.xlabel('Parking Lot')
    plt.ylabel('Number of Spots')
    plt.title('Available vs Occupied Spots per Parking Lot')
    plt.xticks(x, lot_names, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    bar_chart_path = 'static/stacked_bar_lots.png'
    plt.savefig(bar_chart_path)
    plt.clf()

    context = {
        'title': 'Summary',
        'lots': lots,
        'bar_chart': bar_chart_path,
        'total_users': total_users,
        'total_parking_lots': total_parking_lots,
        'total_reservations': total_reservations,
    }
    return render_template('summary.html', context=context)

@app.route('/search_parking', methods=['GET'])
def search_parking():
    search_query = request.args.get('search_query', '').strip()
    if not search_query:
        flash('Please enter a search query.', 'warning')
        return redirect(url_for('home'))
    
    # Search for parking lots by name or pincode
    lots = ParkingLot.query.filter(
        (ParkingLot.name.ilike(f'%{search_query}%')) |
        (ParkingLot.pincode.ilike(f'%{search_query}%'))
    ).all()
    
    if not lots:
        flash('No parking lots found for the given search query.', 'info')
    
    user_email = session.get('email', None)
    user_name = None
    if user_email:
        user = User.query.filter_by(email=user_email).first()
        if user:
            user_name = user.name
            reservations = Reservation.query.filter_by(user_id=user.id).order_by(Reservation.start_time.desc())
    else:
        reservations = None
        user_name = None
    context = {
        'title': 'Search Results',
        'lots': lots,
        'search_query': search_query,
        'name': user_name,
        'reservations': reservations,
        'dateTime': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    return render_template('home.html', context=context)

@app.route('/book_spot/<int:lot_id>', methods=['POST'])
def book_spot(lot_id):
    if request.method == 'POST':
        spot_id = request.form.get('spot_id')
        vehicle_number = request.form.get('vehicle_number')
        user_email = session.get('email', None)
        if not user_email:
            flash('You need to be logged in to book a parking spot.', 'danger')
            return redirect(url_for('home'))
        if user_email:
            user = User.query.filter_by(email=user_email).first()
        spot = ParkingSpot.query.get(spot_id)
        spot.status = 'B'  # Mark the spot as booked
        new_reservation = Reservation(
            spot_id=spot_id,
            user_id=user.id,
            vehicle_number=vehicle_number,
            start_time=datetime.now(),
        )
        db.session.add(new_reservation)
        # Commit changes to the database    
        db.session.commit()
        flash('Parking spot booked successfully!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Invalid request method.', 'danger')
        return redirect(url_for('home'))
    
@app.route('/change_status/<int:reservation_id>', methods=['POST'])
def change_status(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    if request.method == 'POST':
        if request.form.get('status') == 'A':
            reservation.spot.status = 'A'  # Mark the spot as available
            reservation.end_time = datetime.now()
            reservation.cost = reservation.estimated_cost() # calculating cost when releasing the spot
            reservation.status = 'Parked Out'
            db.session.commit()
            flash('Parking spot released successfully!', 'success')
        else:
            reservation.spot.status = 'O'  # Mark the spot as occupied
            # reservation.start_time = datetime.now() >> Error in in the initial logic
            reservation.cost = None  # Initially cost is None when occupied
            reservation.status = 'Occupied'
            db.session.commit()
            flash('Parking spot occupied successfully!', 'success')
        return redirect(url_for('home'))

@app.route('/user/summary', methods=['GET'])
def user_summary():
    user_email = session.get('email', None)
    if not user_email:
        flash('You need to be logged in to view your summary.', 'danger')
        return redirect(url_for('home'))
    
    user = User.query.filter_by(email=user_email).first()
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('home'))
    
    L=[]
    reservations = Reservation.query.filter_by(user_id=user.id).all()
    for reservation in reservations:
        L.append(reservation.estimated_cost())
    print(L)
    histogram = plt.hist(L,bins=10,histtype='barstacked', color='blue', alpha=0.7)
    plt.title('Cost Distribution of Reservations')
    plt.xlabel('Cost')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.75)
    fileName = f'static/histogram_{user.id}.png'
    plt.savefig(fileName)
    context = {
        'title': 'User Summary',
        'user': user,
        'reservations': reservations,
        'histogram_image': fileName,
    }
    
    return render_template('user_summary.html', context=context)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user_email = session.get('email', None)
    user = User.query.filter_by(email=user_email).first() if user_email else None

    if request.method == 'GET':
        return render_template('edit_profile.html', user=user)

    if not user_email:
        flash('You need to be logged in to update your profile.', 'danger')
        return redirect(url_for('home'))
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.address = request.form.get('address')
        user.pincode = request.form.get('pincode')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('home'))