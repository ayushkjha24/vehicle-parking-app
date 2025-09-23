from flask import Flask, render_template
from controller.database import db
from controller.config import Config
from controller.models import *

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
db.init_app(app)

# Ensure database and admin user are created at cold start (not per request)
with app.app_context():
    db.create_all()
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(
            email='admin@example.com',
            password='admin123',  # For demo only; use hashed passwords in production
            name='Admin',
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()

from controller.auth_routes import *
from controller.routes import *