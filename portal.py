from flask import Flask
from flask_apscheduler import APScheduler
import logging
from models import db
from routes import routes
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"

# Add these lines to set the secret key
# app.config['SECRET_KEY'] = os.urandom(24)
# Alternatively, you can set a fixed secret key (less secure but easier for development)
app.config["SECRET_KEY"] = "20092024"
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static/uploads")

db.init_app(app)

logging.basicConfig(level=logging.DEBUG)

# Initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Register the routes Blueprint
app.register_blueprint(routes)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
