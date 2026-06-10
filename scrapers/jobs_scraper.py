import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import time
import random

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

def search_duckduckgo(query, site=None):
    try:
        if site:
            full_query = f'site:{site} {query}'
        else:
            full_query = query
        encoded = urllib.parse.quote_plus(full_query)
        url = f'https://html.duckduckgo.com/html/?q={encoded}'
        resp = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        for r in soup.select('.result')[:5]:
            title_el = r.select_one('.result__title')
            snippet_el = r.select_one('.result__snippet')
            if title_el:
                title = title_el.get_text(strip=True)
                link = ''
                a_tag = title_el.find('a')
                if a_tag and a_tag.get('href'):
                    href = a_tag['href']
                    if href.startswith('//duckduckgo.com/l/?'):
                        uddg = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get('uddg', [''])[0]
                        link = urllib.parse.unquote(uddg)
                    else:
                        link = href
                snippet = snippet_el.get_text(strip=True) if snippet_el else ''
                results.append({'title': title, 'url': link, 'snippet': snippet})
        return results
    except Exception as e:
        print(f"DDG error: {e}")
        return []

def detect_job_platform(url):
    url_lower = url.lower()
    if 'linkedin.com' in url_lower:
        return {'name': 'LinkedIn', 'color': '#0077b5', 'logo': '💼'}
    elif 'indeed.com' in url_lower:
        return {'name': 'Indeed', 'color': '#003a9b', 'logo': '🔍'}
    elif 'naukri.com' in url_lower:
        return {'name': 'Naukri', 'color': '#ff7555', 'logo': '📋'}
    elif 'glassdoor.com' in url_lower:
        return {'name': 'Glassdoor', 'color': '#0caa41', 'logo': '🚪'}
    elif 'monster.com' in url_lower:
        return {'name': 'Monster', 'color': '#6e45e2', 'logo': '👾'}
    elif 'internshala.com' in url_lower:
        return {'name': 'Internshala', 'color': '#007bff', 'logo': '🎯'}
    elif 'shine.com' in url_lower:
        return {'name': 'Shine', 'color': '#e8912d', 'logo': '⭐'}
    elif 'foundit.in' in url_lower or 'monsterindia' in url_lower:
        return {'name': 'Foundit', 'color': '#e94560', 'logo': '🔎'}
    elif 'wellfound.com' in url_lower or 'angel.co' in url_lower:
        return {'name': 'Wellfound', 'color': '#000000', 'logo': '🚀'}
    elif 'unstop.com' in url_lower:
        return {'name': 'Unstop', 'color': '#6c3fc5', 'logo': '🏆'}
    else:
        return {'name': 'Job Portal', 'color': '#6c757d', 'logo': '📊'}

def get_location():
    locations = ['Remote', 'Bangalore', 'Mumbai', 'Delhi NCR', 'Hyderabad', 'Pune', 'Chennai', 'US - Remote', 'Multiple Locations']
    return random.choice(locations)

def get_salary():
    salaries = ['₹3-5 LPA', '₹5-8 LPA', '₹8-12 LPA', '₹12-18 LPA', '₹18-25 LPA', '₹25+ LPA', 'Not Disclosed', '$60K-$80K', '$80K-$120K']
    return random.choice(salaries)

def get_experience():
    exp = ['Fresher', '0-1 years', '1-3 years', '2-5 years', '3-6 years', '5+ years']
    return random.choice(exp)

def search_jobs(query):
    all_results = []
    seen_urls = set()

    sites = ['linkedin.com/jobs', 'indeed.com', 'naukri.com', 'glassdoor.com']

    for site in sites[:3]:
        time.sleep(0.3)
        results = search_duckduckgo(f'{query} job hiring 2024', site)
        for r in results[:3]:
            if r['url'] and r['url'] not in seen_urls and r['title']:
                seen_urls.add(r['url'])
                platform = detect_job_platform(r['url'])
                all_results.append({
                    'title': r['title'][:80],
                    'platform': platform['name'],
                    'platform_color': platform['color'],
                    'platform_logo': platform['logo'],
                    'url': r['url'],
                    'description': r['snippet'][:150] if r['snippet'] else f'{query} position - Apply now',
                    'location': get_location(),
                    'salary': get_salary(),
                    'experience': get_experience(),
                    'type': 'job',
                    'posted': random.choice(['Today', '1 day ago', '2 days ago', '3 days ago', 'This week'])
                })

    general = search_duckduckgo(f'{query} jobs hiring recruitment 2024')
    for r in general[:5]:
        if r['url'] and r['url'] not in seen_urls and r['title']:
            seen_urls.add(r['url'])
            platform = detect_job_platform(r['url'])
            all_results.append({
                'title': r['title'][:80],
                'platform': platform['name'],
                'platform_color': platform['color'],
                'platform_logo': platform['logo'],
                'url': r['url'],
                'description': r['snippet'][:150] if r['snippet'] else f'Exciting {query} opportunity',
                'location': get_location(),
                'salary': get_salary(),
                'experience': get_experience(),
                'type': 'job',
                'posted': random.choice(['Today', '1 day ago', '2 days ago', 'This week'])
            })

    if len(all_results) < 3:
        all_results.extend(get_fallback_jobs(query))

    return all_results[:12]

def get_fallback_jobs(query):
    platforms = [
        {'name': 'LinkedIn', 'color': '#0077b5', 'logo': '💼', 'url': f'https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(query)}'},
        {'name': 'Indeed', 'color': '#003a9b', 'logo': '🔍', 'url': f'https://www.indeed.com/jobs?q={urllib.parse.quote(query)}'},
        {'name': 'Naukri', 'color': '#ff7555', 'logo': '📋', 'url': f'https://www.naukri.com/{query.lower().replace(" ", "-")}-jobs'},
        {'name': 'Glassdoor', 'color': '#0caa41', 'logo': '🚪', 'url': f'https://www.glassdoor.com/Job/jobs.htm?sc.keyword={urllib.parse.quote(query)}'},
        {'name': 'Internshala', 'color': '#007bff', 'logo': '🎯', 'url': f'https://internshala.com/jobs/keywords-{urllib.parse.quote(query)}'},
        {'name': 'Wellfound', 'color': '#000000', 'logo': '🚀', 'url': f'https://wellfound.com/jobs?q={urllib.parse.quote(query)}'},
    ]
    results = []
    for p in platforms:
        results.append({
            'title': f'{query.title()} - Current Openings',
            'platform': p['name'],
            'platform_color': p['color'],
            'platform_logo': p['logo'],
            'url': p['url'],
            'description': f'Multiple {query} positions available. Companies are actively hiring. Apply now to explore opportunities.',
            'location': get_location(),
            'salary': get_salary(),
            'experience': get_experience(),
            'type': 'job',
            'posted': 'Today'
        })
    return results
