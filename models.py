from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(100))
    text = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100))

    def __repr__(self):
        return f"<Post {self.title}>"
