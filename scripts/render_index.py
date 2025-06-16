from jinja2 import Environment, FileSystemLoader
import os
import yaml
from datetime import datetime
import pytz
from dateutil import parser as date_parser

# Setup Jinja environment
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index_template_jinja.html')

def render_index(entries, output_path='index.html'):
    ist_now = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S IST')

    stats = {
        'article_count': len(entries),
        'new_today': sum(1 for e in entries if date_parser.parse(e['fetched_at']).date() == datetime.now(pytz.timezone('Asia/Kolkata')).date()),
        'categories': {}
    }

    for entry in entries:
        cat = entry.get('category', 'Technology')
        stats['categories'][cat] = stats['categories'].get(cat, 0) + 1

    featured_article = entries[0] if entries else None

    rendered_html = template.render(
        title="BBC Tech Digest",
        entries=entries[1:],
        featured_article=featured_article,
        last_updated=ist_now,
        stats=stats
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

    print(f"✅ index.html rendered to {output_path}")
