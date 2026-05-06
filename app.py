import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_bcrypt import Bcrypt
from database.models import db, User, DailyLog, BrowserSyncToken, BrowserActivity
from utils.gemini_service import generate_insights
from utils.chrome_analyzer import analyze_chrome_history
from utils.browser_intelligence import classify_domain, calculate_category_breakdown, get_top_sites, estimate_productivity_impact
from dotenv import load_dotenv
import joblib
import pandas as pd
from datetime import datetime, date, timedelta
import secrets
import hashlib

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback_dev_secret_key')

# Use /tmp for SQLite on Vercel (serverless has read-only filesystem)
IS_VERCEL = os.environ.get('VERCEL', False)
if IS_VERCEL:
    DB_PATH = '/tmp/site.db'
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'site.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)

# Load ML model (use absolute path for Vercel compatibility)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'rf_model.joblib')
try:
    rf_model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Warning: Could not load ML model. {e}")
    rf_model = None

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('signup'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash('Account created! You are now able to log in', 'success')
        return redirect(url_for('login'))
        
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    study_hours = float(data.get('study_hours', 0))
    work_hours = float(data.get('work_hours', 0))
    screen_time = float(data.get('screen_time', 0))
    distraction_time = float(data.get('distraction_time', 0))
    sleep_hours = float(data.get('sleep_hours', 0))
    
    # Feature engineering for the model
    productivity_ratio = (study_hours + work_hours) / (screen_time + 0.1)
    distraction_ratio = distraction_time / (study_hours + work_hours + 0.1)
    consistency_score = sleep_hours / 8.0
    
    features = pd.DataFrame([{
        'study_hours': study_hours,
        'work_hours': work_hours,
        'screen_time': screen_time,
        'distraction_time': distraction_time,
        'sleep_hours': sleep_hours,
        'productivity_ratio': productivity_ratio,
        'distraction_ratio': distraction_ratio,
        'consistency_score': consistency_score
    }])
    
    if rf_model:
        score = float(rf_model.predict(features)[0])
    else:
        score = 50.0 # Fallback
        
    # Save log
    log = DailyLog(
        user_id=session['user_id'],
        study_hours=study_hours,
        work_hours=work_hours,
        screen_time=screen_time,
        distraction_time=distraction_time,
        sleep_hours=sleep_hours,
        productivity_score=score
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'score': score, 'log_id': log.id})

@app.route('/insights', methods=['POST'])
def insights():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.json
    log_id = data.get('log_id')
    is_roast_mode = data.get('roast_mode', False)
    
    log = DailyLog.query.get(log_id)
    if not log or log.user_id != session['user_id']:
        return jsonify({'error': 'Log not found'}), 404
        
    log_data = {
        'study_hours': log.study_hours,
        'work_hours': log.work_hours,
        'screen_time': log.screen_time,
        'distraction_time': log.distraction_time,
        'sleep_hours': log.sleep_hours,
        'productivity_score': log.productivity_score
    }
    
    insights_data = generate_insights(log_data, is_roast_mode)
    
    return jsonify(insights_data)

@app.route('/history', methods=['GET'])
def history():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    logs = DailyLog.query.filter_by(user_id=session['user_id']).order_by(DailyLog.date.asc()).all()
    
    data = []
    for log in logs:
        data.append({
            'date': log.date.strftime('%Y-%m-%d'),
            'score': log.productivity_score,
            'productive_time': log.study_hours + log.work_hours,
            'distraction_time': log.distraction_time
        })
        
    return jsonify(data)

@app.route('/export-csv', methods=['GET'])
def export_csv():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    import io
    import csv
    
    logs = DailyLog.query.filter_by(user_id=session['user_id']).order_by(DailyLog.date.asc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Study Hours', 'Work Hours', 'Screen Time', 'Distraction Time', 'Sleep Hours', 'Productivity Score'])
    
    for log in logs:
        writer.writerow([
            log.date.strftime('%Y-%m-%d'),
            log.study_hours,
            log.work_hours,
            log.screen_time,
            log.distraction_time,
            log.sleep_hours,
            round(log.productivity_score, 1)
        ])
    
    output.seek(0)
    from flask import Response
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=productivity_report.csv'}
    )

@app.route('/clear-logs', methods=['POST'])
def clear_logs():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    DailyLog.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    
    return jsonify({'message': 'All activity logs cleared successfully.'})

@app.route('/download-extension')
def download_extension():
    """Serve the MindPulse browser extension as a downloadable ZIP."""
    zip_path = os.path.join(BASE_DIR, 'MindPulse_Extension.zip')
    if not os.path.exists(zip_path):
        return jsonify({'error': 'Extension file not found'}), 404
    return send_file(
        zip_path,
        as_attachment=True,
        download_name='MindPulse_Extension.zip',
        mimetype='application/zip'
    )

@app.route('/chrome-history', methods=['GET'])
def chrome_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    hours = request.args.get('hours', 24, type=int)
    data = analyze_chrome_history(hours=hours)
    return jsonify(data)

@app.route('/api/browser-token/generate', methods=['POST'])
def generate_browser_token():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    user_id = session['user_id']
    
    # Invalidate old active tokens
    BrowserSyncToken.query.filter_by(user_id=user_id, is_active=True).update({'is_active': False})
    
    raw_token = "mp_live_" + secrets.token_hex(20)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    
    new_token = BrowserSyncToken(
        user_id=user_id,
        token_prefix=raw_token[:12],
        token_hash=token_hash,
        is_active=True
    )
    db.session.add(new_token)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "token": raw_token
    })

@app.route('/api/browser-token/revoke', methods=['POST'])
def revoke_browser_token():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    BrowserSyncToken.query.filter_by(user_id=session['user_id'], is_active=True).update({'is_active': False})
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "Browser sync token revoked"
    })

@app.route('/api/browser-history/sync', methods=['POST'])
def sync_browser_history():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing or invalid token'}), 401
        
    token = auth_header.split(' ')[1]
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    
    active_token = BrowserSyncToken.query.filter_by(token_hash=token_hash, is_active=True).first()
    if not active_token:
        return jsonify({'error': 'Invalid or revoked token'}), 401
        
    # Update last used
    active_token.last_used_at = datetime.utcnow()
    user_id = active_token.user_id
    
    data = request.json
    events = data.get('events', [])
    source = data.get('source', 'chrome_extension')
    
    saved = 0
    skipped = 0
    
    for event in events:
        try:
            # Parse last_visit_time
            lvt = datetime.fromisoformat(event['last_visit_time'].replace('Z', '+00:00'))
            # Remove timezone info to match sqlite naive datetime
            lvt = lvt.replace(tzinfo=None)
            
            # Check for duplicates based on user, url/domain, and exact time
            existing = BrowserActivity.query.filter_by(
                user_id=user_id,
                domain=event['domain'],
                last_visit_time=lvt
            ).first()
            
            if existing:
                skipped += 1
                continue
                
            activity = BrowserActivity(
                user_id=user_id,
                domain=event['domain'],
                url=event.get('url', event['domain']),
                title=event.get('title', ''),
                category=classify_domain(event['domain']),
                last_visit_time=lvt,
                visit_count=event.get('visit_count', 1),
                typed_count=event.get('typed_count', 0),
                source=source
            )
            db.session.add(activity)
            saved += 1
        except Exception as e:
            skipped += 1
            continue
            
    db.session.commit()
    
    return jsonify({
        "success": True,
        "saved": saved,
        "skipped": skipped
    })

@app.route('/api/browser-history/analytics', methods=['GET'])
def browser_analytics():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    user_id = session['user_id']
    hours = request.args.get('hours', 24, type=int)
    
    summary = calculate_category_breakdown(user_id, hours)
    top_sites = get_top_sites(user_id, hours, limit=10)
    
    return jsonify({
        "success": True,
        "range_hours": hours,
        "summary": summary,
        "top_sites": top_sites,
        "category_breakdown": {
            "productive": summary['productive_count'],
            "distraction": summary['distraction_count'],
            "neutral": summary['neutral_count']
        }
    })

@app.route('/streak', methods=['GET'])
def streak():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    logs = DailyLog.query.filter_by(user_id=session['user_id']).order_by(DailyLog.date.asc()).all()
    
    if not logs:
        return jsonify({
            'current_streak': 0,
            'longest_streak': 0,
            'total_logs': 0,
            'heatmap': {},
            'avg_score': 0
        })
    
    # Get unique dates with logs
    log_dates = sorted(set(log.date for log in logs))
    
    # Calculate current streak (consecutive days ending today or yesterday)
    today = date.today()
    current_streak = 0
    check_date = today
    
    # Allow for today not yet being logged
    if check_date not in log_dates and (check_date - timedelta(days=1)) in log_dates:
        check_date = check_date - timedelta(days=1)
    
    while check_date in log_dates:
        current_streak += 1
        check_date -= timedelta(days=1)
    
    # Calculate longest streak
    longest_streak = 0
    temp_streak = 1
    for i in range(1, len(log_dates)):
        if (log_dates[i] - log_dates[i-1]).days == 1:
            temp_streak += 1
        else:
            longest_streak = max(longest_streak, temp_streak)
            temp_streak = 1
    longest_streak = max(longest_streak, temp_streak)
    
    # Build heatmap data (last 90 days)
    heatmap = {}
    ninety_days_ago = today - timedelta(days=90)
    for log in logs:
        if log.date >= ninety_days_ago:
            date_str = log.date.strftime('%Y-%m-%d')
            # Keep the highest score if multiple logs per day
            if date_str not in heatmap or log.productivity_score > heatmap[date_str]:
                heatmap[date_str] = round(log.productivity_score, 1)
    
    # Average score
    scores = [log.productivity_score for log in logs]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
    
    return jsonify({
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'total_logs': len(log_dates),
        'heatmap': heatmap,
        'avg_score': avg_score
    })

# Vercel uses the `app` object directly as WSGI application
if __name__ == '__main__':
    app.run(debug=True, port=5000)
