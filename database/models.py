from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    logs = db.relationship('DailyLog', backref='user', lazy=True)

class DailyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    
    # Inputs
    study_hours = db.Column(db.Float, nullable=False)
    work_hours = db.Column(db.Float, nullable=False)
    screen_time = db.Column(db.Float, nullable=False)
    distraction_time = db.Column(db.Float, nullable=False)
    sleep_hours = db.Column(db.Float, nullable=False)
    
    # Outputs
    productivity_score = db.Column(db.Float, nullable=False)
    insights = db.Column(db.Text, nullable=True)

class BrowserSyncToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token_prefix = db.Column(db.String(20), nullable=False)
    token_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

class BrowserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(2048), nullable=False)
    title = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(50), nullable=False) # productive, distraction, neutral
    last_visit_time = db.Column(db.DateTime, nullable=False)
    visit_count = db.Column(db.Integer, default=1)
    typed_count = db.Column(db.Integer, default=0)
    source = db.Column(db.String(50), default='chrome_extension')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
