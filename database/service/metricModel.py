from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MetricModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    connection_count = db.Column(db.Integer)
    cpu = db.Column(db.Float)
    ram = db.Column(db.Float)
    status = db.Column(db.String)
    error_text = db.Column(db.String)
