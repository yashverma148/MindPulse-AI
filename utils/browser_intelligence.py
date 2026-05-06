from datetime import datetime, timedelta
import urllib.parse
from database.models import BrowserActivity

PRODUCTIVE_DOMAINS = {
    'github.com', 'stackoverflow.com', 'leetcode.com', 'kaggle.com', 
    'coursera.org', 'udemy.com', 'edx.org', 'docs.python.org', 
    'developer.mozilla.org', 'w3schools.com', 'geeksforgeeks.org', 
    'medium.com', 'notion.so', 'figma.com', 'openai.com'
}

DISTRACTION_DOMAINS = {
    'youtube.com', 'instagram.com', 'facebook.com', 'netflix.com', 
    'primevideo.com', 'reddit.com', 'x.com', 'twitter.com', 
    'tiktok.com', 'snapchat.com'
}

def normalize_domain(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return ""

def classify_domain(domain):
    if not domain:
        return 'neutral'
        
    domain_lower = domain.lower()
    
    # Exact match or subdomain match
    for prod_domain in PRODUCTIVE_DOMAINS:
        if domain_lower == prod_domain or domain_lower.endswith('.' + prod_domain):
            return 'productive'
            
    for dist_domain in DISTRACTION_DOMAINS:
        if domain_lower == dist_domain or domain_lower.endswith('.' + dist_domain):
            return 'distraction'
            
    return 'neutral'

def calculate_category_breakdown(user_id, hours):
    time_limit = datetime.utcnow() - timedelta(hours=hours)
    
    activities = BrowserActivity.query.filter(
        BrowserActivity.user_id == user_id,
        BrowserActivity.last_visit_time >= time_limit
    ).all()
    
    breakdown = {
        'productive': 0,
        'distraction': 0,
        'neutral': 0
    }
    
    total_visits = 0
    
    for activity in activities:
        breakdown[activity.category] += activity.visit_count
        total_visits += activity.visit_count
        
    productivity_ratio = (breakdown['productive'] / total_visits * 100) if total_visits > 0 else 0
    distraction_ratio = (breakdown['distraction'] / total_visits * 100) if total_visits > 0 else 0
    
    return {
        'productive_count': breakdown['productive'],
        'distraction_count': breakdown['distraction'],
        'neutral_count': breakdown['neutral'],
        'total_visits': total_visits,
        'productivity_ratio': round(productivity_ratio, 1),
        'distraction_ratio': round(distraction_ratio, 1)
    }

def get_top_sites(user_id, hours, limit=10):
    time_limit = datetime.utcnow() - timedelta(hours=hours)
    
    activities = BrowserActivity.query.filter(
        BrowserActivity.user_id == user_id,
        BrowserActivity.last_visit_time >= time_limit
    ).all()
    
    domain_counts = {}
    domain_categories = {}
    
    for activity in activities:
        if activity.domain not in domain_counts:
            domain_counts[activity.domain] = 0
            domain_categories[activity.domain] = activity.category
            
        domain_counts[activity.domain] += activity.visit_count
        
    sorted_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    result = []
    for domain, count in sorted_domains:
        result.append({
            'domain': domain,
            'category': domain_categories[domain],
            'visits': count
        })
        
    return result

def estimate_productivity_impact(user_id, hours):
    summary = calculate_category_breakdown(user_id, hours)
    if summary['total_visits'] == 0:
        return 50.0 # Neutral fallback
        
    # Simple metric: ratio of productive to (productive + distraction) scaled to 0-100
    prod = summary['productive_count']
    dist = summary['distraction_count']
    
    if prod + dist == 0:
        return 50.0
        
    score = (prod / (prod + dist)) * 100
    return round(score, 1)
