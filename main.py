from flask import Flask,render_template
from controller.database import db
from controller.config import Config
from controller.models import *


app = Flask(__name__,template_folder='templates',static_folder='static')
app.config.from_object(Config)
db.init_app(app)


with app.app_context():
    db.create_all()

    if not User.query.filter_by(email='admin@example.com').first():
            admin = User(
                email='admin@example.com',
                password='admin123',  # or plain text for demo
                name='Admin',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()

from controller.auth_routes import *
from controller.routes import *


if __name__ == '__main__':
    app.run()