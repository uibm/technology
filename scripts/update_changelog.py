#!/usr/bin/env python3

import feedparser
import yaml
from datetime import datetime
import os
from dateutil import parser
import pytz
import time
import hashlib
import sys
import requests
from bs4 import BeautifulSoup
import re
from render_index import render_index

def generate_entry_hash(data):
    content = f"{data.get('title', '')}{data.get('summary', '')}{data.get('link', '')}"
    return hashlib.md5(content.encode()).hexdigest()

def extract_image_from_content(content, link):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        img_tag = soup.find('img')
        if img_tag and img_tag.get('src'):
            return img_tag['src']

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(link, headers=headers, timeout=10)
        if response.status_code == 200:
            page_soup = BeautifulSoup(response.content, 'html.parser')
            selectors = [
                'meta[property="og:image"]',
                'img[data-component="image"]',
                '.story-body__image img',
                'figure img'
            ]
            for selector in selectors:
                img_element = page_soup.select_one(selector)
                if img_element:
                    img_url = img_element.get('content') or img_element.get('src')
                    if img_url:
                        return img_url if img_url.startswith('http') else f"https://www.bbc.com{img_url}"
    except Exception as e:
        print(f"Image extraction error for {link}: {e}")

    return "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=250&fit=crop"

def categorize_article(title, summary):
    content = f"{title} {summary}".lower()
    categories = {
        'AI & Machine Learning': ['ai', 'artificial intelligence', 'machine learning', 'chatgpt', 'openai', 'neural', 'algorithm'],
        'Cybersecurity': ['security', 'hack', 'breach', 'cyber', 'malware', 'phishing'],
        'Mobile & Apps': ['iphone', 'android', 'app', 'mobile', 'smartphone', 'ios'],
        'Social Media': ['facebook', 'twitter', 'instagram', 'tiktok', 'social media', 'meta'],
        'Gaming': ['game', 'gaming', 'xbox', 'playstation', 'nintendo', 'esports'],
        'Business & Finance': ['startup', 'investment', 'funding', 'ipo', 'business', 'revenue'],
        'Hardware': ['chip', 'processor', 'hardware', 'device'],
        'Software': ['software', 'update', 'version', 'release', 'platform']
    }
    for category, keywords in categories.items():
        if any(keyword in content for keyword in keywords):
            return category
    return 'Technology'

def load_existing_entries():
    if os.path.exists('_data/changelog.yml'):
        with open('_data/changelog.yml', 'r', encoding='utf-8') as f:
            try:
                entries = yaml.safe_load(f) or []
                for entry in entries:
                    if 'hash' not in entry:
                        entry['hash'] = generate_entry_hash(entry)
                return entries
            except yaml.YAMLError as e:
                print(f"Error loading YAML: {e}", file=sys.stderr)
                return []
    return []

def fetch_bbc_feed():
    for attempt in range(3):
        try:
            feed = feedparser.parse('https://feeds.bbci.co.uk/news/technology/rss.xml')
            if hasattr(feed, 'status') and feed.status == 200:
                return feed.entries
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)
    return []

def create_changelog_entry(entry):
    ist_tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist_tz)
    word_count = len(entry.summary.split())
    reading_time = max(1, round(word_count / 200))
    return {
        'title': entry.title,
        'link': entry.link,
        'published': parser.parse(entry.published).astimezone(ist_tz).isoformat(),
        'summary': entry.summary,
        'guid': entry.guid,
        'hash': generate_entry_hash(entry),
        'timestamp': current_time.isoformat(),
        'fetched_at': current_time.strftime('%Y-%m-%d %H:%M:%S IST'),
        'image_url': extract_image_from_content(entry.get('content', [{}])[0].get('value', '') if entry.get('content') else '', entry.link),
        'category': categorize_article(entry.title, entry.summary),
        'reading_time': f"{reading_time} min read",
        'author': entry.get('author', 'BBC Technology'),
        'tags': list(set(re.findall(r'\b(?:AI|tech|data|cyber|mobile|app|software|hardware|startup|innovation)\b', f"{entry.title} {entry.summary}", re.IGNORECASE)))[:3]
    }

def update_changelog():
    print(f"Updating changelog at {datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S IST')}")
    existing_entries = load_existing_entries()
    existing_hashes = {entry['hash'] for entry in existing_entries}
    new_entries = fetch_bbc_feed()

    updates = [create_changelog_entry(e) for e in new_entries if generate_entry_hash(e) not in existing_hashes]

    all_entries = updates + existing_entries
    all_entries.sort(key=lambda x: x['published'], reverse=True)
    all_entries = all_entries[:100]

    with open('_data/changelog.yml', 'w', encoding='utf-8') as f:
        yaml.dump(all_entries, f, allow_unicode=True, sort_keys=False)

    render_index(all_entries, output_path="index.html")

    return len(updates) > 0

if __name__ == '__main__':
    try:
        update_changelog()
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)