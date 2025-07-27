# Vehicle Parking App - V1

## Overview

Vehicle Parking App is a multi-user web application for managing 4-wheeler parking lots, spots, and parked vehicles. The app supports two roles: **Administrator** (superuser) and **User**. It is built using Flask (backend), Jinja2/HTML/CSS/Bootstrap (frontend), and SQLite (database). All database tables are created programmatically.

---

## Roles & Features

### Admin (Superuser)
- No registration required; admin exists when the database is created.
- Can create, edit, and delete parking lots.
- Can set the number of parking spots per lot (spots are auto-created).
- Can set different prices for each lot.
- Can view status of all parking spots and parked vehicle details.
- Can view all registered users.
- Can view summary charts of parking lots/spots.

### User
- Can register and login.
- Can view available parking lots.
- Can book a spot (auto-allocation of first available spot).
- Can occupy and release a spot (status changes, timestamps recorded).
- Can view parking history and summary charts.

---

## Database Models

- **User:** Stores user info, login credentials, and reservations.
- **ParkingLot:** Stores lot details, price, address, pincode, and manages spots.
- **ParkingSpot:** Stores spot status (Available/Occupied) and reservation.
- **Reservation:** Stores booking info, timestamps, cost, and links to user and spot.

---

## Core Functionalities

- **Authentication:** Separate login/register for users, admin login for superuser.
- **Admin Dashboard:** Manage lots/spots, view user and parking details, summary charts.
- **User Dashboard:** View lots, book/release spots, track parking history, summary charts.
- **Spot Allocation:** Users are auto-assigned the first available spot in a selected lot.
- **Status & Timestamps:** Spot status changes (Occupied/Available), timestamps recorded for parking in/out.
- **Cost Calculation:** Parking cost calculated based on duration and lot price.
- **Charts:** Summary charts for lots and user parking history.

---

## Technologies Used

- **Backend:** Flask
- **Frontend:** Jinja2, HTML, CSS, Bootstrap
- **Database:** SQLite (created via models, no manual DB creation)

---

## Setup Instructions

1. Clone the repository.
2. Install dependencies:  
   `pip install -r requirements.txt`
3. Run the database setup script (tables are created programmatically).
4. Start the Flask server:  
   `python main.py`
5. Access the app at `http://127.0.0.1:5000/`

---

## Folder Structure
.
├── controller
│   ├── auth_routes.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── __pycache__
│   │   ├── auth_routes.cpython-313.pyc
│   │   ├── config.cpython-312.pyc
│   │   ├── config.cpython-313.pyc
│   │   ├── database.cpython-312.pyc
│   │   ├── database.cpython-313.pyc
│   │   ├── models.cpython-312.pyc
│   │   ├── models.cpython-313.pyc
│   │   └── routes.cpython-313.pyc
│   └── routes.py
├── instance
│   └── database.sqlite3
├── main.py
├── __pycache__
│   └── main.cpython-313.pyc
├── README.md
├── requirement.txt
├── static
│   └── style.css
└── templates
    ├── admin_dashboard.html
    ├── base.html
    ├── home.html
    ├── login.html
    ├── navbar.html
    ├── parking_lot.html
    ├── parkings.html
    ├── register.html
    ├── reservations.html
    ├── search.html
    ├── summary.html
    ├── user_dashboard.html
    ├── users.html
    └── user_summary.html

## Notes

- All demos run locally.
- Admin is predefined; no registration required.
- Database must be created via model code, not manually.
- Wireframes are for flow reference only; UI design is flexible.

---

## Reference

- [Secure Parking India](https://www.secureparking.co.in/)

---

## License

For educational use (MAD-I).

---

**Contact:**  
For queries or collaboration, reach out to the project