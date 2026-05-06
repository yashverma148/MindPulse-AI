import os
import sqlite3
import shutil
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from urllib.parse import urlparse

# Categories for website classification
PRODUCTIVE_DOMAINS = {
    'github.com', 'stackoverflow.com', 'leetcode.com', 'kaggle.com',
    'docs.python.org', 'developer.mozilla.org', 'w3schools.com',
    'coursera.org', 'udemy.com', 'edx.org', 'khanacademy.org',
    'medium.com', 'dev.to', 'hashnode.dev', 'notion.so',
    'google.com/search', 'scholar.google.com', 'arxiv.org',
    'docs.google.com', 'drive.google.com', 'figma.com',
    'linkedin.com', 'glassdoor.com', 'indeed.com',
    'trello.com', 'asana.com', 'jira.atlassian.net',
    'replit.com', 'codepen.io', 'codesandbox.io',
    'npmjs.com', 'pypi.org', 'huggingface.co',
    'geeksforgeeks.org', 'hackerrank.com', 'codeforces.com',
}

DISTRACTION_DOMAINS = {
    'youtube.com', 'netflix.com', 'reddit.com', 'twitter.com',
    'x.com', 'facebook.com', 'instagram.com', 'tiktok.com',
    'twitch.tv', 'discord.com', 'snapchat.com', 'pinterest.com',
    'buzzfeed.com', '9gag.com', 'tumblr.com',
    'amazon.com', 'flipkart.com', 'myntra.com', 'ajio.com',
    'hotstar.com', 'primevideo.com', 'disneyplus.com',
    'spotify.com', 'soundcloud.com',
}


def get_chrome_history_path():
    """Get the default Chrome History database path for Windows."""
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    if not local_app_data:
        return None
    path = os.path.join(local_app_data, 'Google', 'Chrome', 'User Data', 'Default', 'History')
    if os.path.exists(path):
        return path
    return None


def analyze_chrome_history(hours=24):
    """
    Analyze Chrome browsing history for the last N hours.
    Returns categorized data for the dashboard.
    """
    history_path = get_chrome_history_path()
    if not history_path:
        return {
            'error': 'Chrome history file not found. Make sure Google Chrome is installed.',
            'top_sites': [],
            'productive_count': 0,
            'distraction_count': 0,
            'neutral_count': 0,
            'total_visits': 0,
            'categories': {},
            'hourly_activity': {}
        }

    # Chrome locks the History DB, so we copy it to a temp file
    temp_dir = tempfile.mkdtemp()
    temp_db = os.path.join(temp_dir, 'History_copy')
    
    try:
        shutil.copy2(history_path, temp_db)
    except PermissionError:
        return {
            'error': 'Cannot read Chrome history. Please close Chrome completely and try again.',
            'top_sites': [],
            'productive_count': 0,
            'distraction_count': 0,
            'neutral_count': 0,
            'total_visits': 0,
            'categories': {},
            'hourly_activity': {}
        }

    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        # Chrome stores timestamps as microseconds since Jan 1, 1601
        # Convert current time to Chrome's epoch
        epoch_start = datetime(1601, 1, 1)
        now = datetime.utcnow()
        cutoff = now - timedelta(hours=hours)
        
        chrome_cutoff = int((cutoff - epoch_start).total_seconds() * 1_000_000)

        cursor.execute("""
            SELECT url, title, visit_count, last_visit_time
            FROM urls
            WHERE last_visit_time > ?
            ORDER BY visit_count DESC
        """, (chrome_cutoff,))

        rows = cursor.fetchall()
        conn.close()

        # Process results
        domain_visits = Counter()
        productive_count = 0
        distraction_count = 0
        neutral_count = 0
        categories = defaultdict(int)
        hourly_activity = defaultdict(int)

        for url, title, visit_count, last_visit_time in rows:
            try:
                parsed = urlparse(url)
                domain = parsed.netloc.replace('www.', '')
            except:
                continue

            domain_visits[domain] += visit_count

            # Classify the domain
            is_productive = any(p in domain for p in PRODUCTIVE_DOMAINS)
            is_distraction = any(d in domain for d in DISTRACTION_DOMAINS)

            if is_productive:
                productive_count += visit_count
                categories['Productive'] += visit_count
            elif is_distraction:
                distraction_count += visit_count
                categories['Distraction'] += visit_count
            else:
                neutral_count += visit_count
                categories['Neutral'] += visit_count

            # Hourly activity
            try:
                visit_dt = epoch_start + timedelta(microseconds=last_visit_time)
                hourly_activity[visit_dt.hour] += visit_count
            except:
                pass

        # Top 10 sites
        top_sites = []
        for domain, count in domain_visits.most_common(10):
            site_type = 'neutral'
            if any(p in domain for p in PRODUCTIVE_DOMAINS):
                site_type = 'productive'
            elif any(d in domain for d in DISTRACTION_DOMAINS):
                site_type = 'distraction'

            top_sites.append({
                'domain': domain,
                'visits': count,
                'type': site_type
            })

        total_visits = productive_count + distraction_count + neutral_count

        return {
            'error': None,
            'top_sites': top_sites,
            'productive_count': productive_count,
            'distraction_count': distraction_count,
            'neutral_count': neutral_count,
            'total_visits': total_visits,
            'categories': dict(categories),
            'hourly_activity': dict(hourly_activity)
        }

    except Exception as e:
        print(f"Chrome history analysis error: {e}")
        return {
            'error': f'Error analyzing history: {str(e)}',
            'top_sites': [],
            'productive_count': 0,
            'distraction_count': 0,
            'neutral_count': 0,
            'total_visits': 0,
            'categories': {},
            'hourly_activity': {}
        }
    finally:
        # Clean up temp files
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
