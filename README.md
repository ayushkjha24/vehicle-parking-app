# Vehicle-Parking-App
A multi-user app that manages different parking lots, parking spots and parked vehicles for 4 wheelers.


### Frameworks to be used

 - Flask for application back-end
 - Jinja2 templating, HTML, CSS and Bootstraps for application front-end
 - SQLite for database (No other database is permitted)

### Roles
The platform will have two roles:

1. Admin - root access - It is the superuser of the app and requires no registration

    - Admin is also known as the superuser
    - Admin can create a new parking lot
    - Each parking lot can have any number of parking spots for 4-wheeler parking
    - Each parking lot can have a different price
    - Admin can view the status of all available parking spots on his/her dashboard
    - Admin can edit/delete any number of parking lots, i.e., admin can increase or decrease the number of parking spots inside the lot.

2. User - Can reserve a parking space
    - Register/Login
    - Choose an available parking lot
    - Book the spot (automatically allotted by the app after booking)
    - Release or vacate the spot