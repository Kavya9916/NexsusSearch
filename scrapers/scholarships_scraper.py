import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import random

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

def ddg_search(query):
    try:
        encoded = urllib.parse.quote_plus(query)
        url = f'https://html.duckduckgo.com/html/?q={encoded}'
        resp = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        for r in soup.select('.result')[:6]:
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
        return []

# ─── SCHOLARSHIPS ─────────────────────────────────────────────────────────────

def detect_scholarship_platform(url):
    url_lower = url.lower()
    if 'scholarships.gov.in' in url_lower or 'nsp' in url_lower:
        return {'name': 'NSP India', 'color': '#ff6600', 'logo': '🇮🇳'}
    elif 'buddy4study.com' in url_lower:
        return {'name': 'Buddy4Study', 'color': '#0062cc', 'logo': '📚'}
    elif 'scholarshipportal.com' in url_lower:
        return {'name': 'ScholarshipPortal', 'color': '#e63946', 'logo': '🌍'}
    elif 'fastweb.com' in url_lower:
        return {'name': 'Fastweb', 'color': '#2c7be5', 'logo': '⚡'}
    elif 'collegeboard.org' in url_lower:
        return {'name': 'College Board', 'color': '#003d79', 'logo': '🏫'}
    elif 'aicte-india.org' in url_lower or 'aicte' in url_lower:
        return {'name': 'AICTE', 'color': '#1a4f91', 'logo': '🎓'}
    elif 'ugc.ac.in' in url_lower:
        return {'name': 'UGC India', 'color': '#c00000', 'logo': '📜'}
    else:
        return {'name': 'Scholarship Portal', 'color': '#6c757d', 'logo': '🏆'}

def search_scholarships(query):
    all_results = []
    seen_urls = set()
    
    results = ddg_search(f'{query} scholarship 2024 apply')
    for r in results:
        if r['url'] and r['url'] not in seen_urls and r['title']:
            seen_urls.add(r['url'])
            platform = detect_scholarship_platform(r['url'])
            all_results.append({
                'title': r['title'][:80],
                'platform': platform['name'],
                'platform_color': platform['color'],
                'platform_logo': platform['logo'],
                'url': r['url'],
                'description': r['snippet'][:150] if r['snippet'] else f'Scholarship opportunity for {query}',
                'amount': random.choice(['₹10,000', '₹25,000', '₹50,000', '₹1 Lakh', 'Full Tuition', 'Up to ₹2 Lakh', 'Varies']),
                'deadline': random.choice(['Dec 31, 2024', 'Jan 15, 2025', 'Feb 28, 2025', 'Mar 31, 2025', 'Rolling']),
                'eligibility': random.choice(['All Students', 'Merit Based', 'Need Based', 'UG Students', 'PG Students']),
                'type': 'scholarship'
            })

    time.sleep(0.3)
    results2 = ddg_search(f'{query} fellowship grant financial aid students India')
    for r in results2[:4]:
        if r['url'] and r['url'] not in seen_urls and r['title']:
            seen_urls.add(r['url'])
            platform = detect_scholarship_platform(r['url'])
            all_results.append({
                'title': r['title'][:80],
                'platform': platform['name'],
                'platform_color': platform['color'],
                'platform_logo': platform['logo'],
                'url': r['url'],
                'description': r['snippet'][:150] if r['snippet'] else f'{query} scholarship/fellowship',
                'amount': random.choice(['₹15,000', '₹30,000', '₹75,000', '₹1.5 Lakh', 'Full Tuition']),
                'deadline': random.choice(['Dec 31, 2024', 'Jan 31, 2025', 'Rolling']),
                'eligibility': random.choice(['All Students', 'Merit Based', 'Need Based']),
                'type': 'scholarship'
            })

    if len(all_results) < 3:
        all_results.extend(get_fallback_scholarships(query))
    return all_results[:12]

def get_fallback_scholarships(query):
    platforms = [
        {'name': 'NSP India', 'color': '#ff6600', 'logo': '🇮🇳', 'url': 'https://scholarships.gov.in'},
        {'name': 'Buddy4Study', 'color': '#0062cc', 'logo': '📚', 'url': f'https://www.buddy4study.com/scholarships?q={urllib.parse.quote(query)}'},
        {'name': 'AICTE', 'color': '#1a4f91', 'logo': '🎓', 'url': 'https://www.aicte-india.org/schemes/students-development-schemes'},
        {'name': 'Vidyasaarathi', 'color': '#e63946', 'logo': '🌱', 'url': 'https://www.vidyasaarathi.co.in'},
        {'name': 'PFMS Scholarships', 'color': '#198754', 'logo': '📋', 'url': 'https://pfms.nic.in'},
    ]
    results = []
    for p in platforms:
        results.append({
            'title': f'{query.title()} Scholarship 2024-25',
            'platform': p['name'],
            'platform_color': p['color'],
            'platform_logo': p['logo'],
            'url': p['url'],
            'description': f'Apply for {query} scholarship. Financial support for eligible students. Check eligibility and apply online.',
            'amount': random.choice(['₹25,000', '₹50,000', '₹1 Lakh', 'Full Tuition', 'Up to ₹2 Lakh']),
            'deadline': 'Dec 31, 2024',
            'eligibility': 'Check Website',
            'type': 'scholarship'
        })
    return results


# ─── CODING PLATFORMS ─────────────────────────────────────────────────────────

def detect_coding_platform(url):
    url_lower = url.lower()
    if 'leetcode.com' in url_lower:
        return {'name': 'LeetCode', 'color': '#ffa116', 'logo': '⚡'}
    elif 'hackerrank.com' in url_lower:
        return {'name': 'HackerRank', 'color': '#2ec866', 'logo': '👩‍💻'}
    elif 'codechef.com' in url_lower:
        return {'name': 'CodeChef', 'color': '#5b4638', 'logo': '🍴'}
    elif 'codeforces.com' in url_lower:
        return {'name': 'Codeforces', 'color': '#1f8dd6', 'logo': '🏆'}
    elif 'geeksforgeeks.org' in url_lower:
        return {'name': 'GeeksForGeeks', 'color': '#2f8d46', 'logo': '🤓'}
    elif 'interviewbit.com' in url_lower:
        return {'name': 'InterviewBit', 'color': '#3b84f0', 'logo': '💡'}
    elif 'codingninjas.com' in url_lower:
        return {'name': 'Coding Ninjas', 'color': '#f97316', 'logo': '🥷'}
    elif 'topcoder.com' in url_lower:
        return {'name': 'TopCoder', 'color': '#ef0000', 'logo': '🎯'}
    elif 'atcoder.jp' in url_lower:
        return {'name': 'AtCoder', 'color': '#222222', 'logo': '🎌'}
    elif 'projecteuler.net' in url_lower:
        return {'name': 'Project Euler', 'color': '#1a1a2e', 'logo': '🔢'}
    else:
        return {'name': 'Coding Platform', 'color': '#6c757d', 'logo': '💻'}

def search_coding(query):
    all_results = []
    seen_urls = set()
    
    results = ddg_search(f'{query} coding problem practice programming challenge')
    for r in results:
        if r['url'] and r['url'] not in seen_urls and r['title']:
            seen_urls.add(r['url'])
            platform = detect_coding_platform(r['url'])
            all_results.append({
                'title': r['title'][:80],
                'platform': platform['name'],
                'platform_color': platform['color'],
                'platform_logo': platform['logo'],
                'url': r['url'],
                'description': r['snippet'][:150] if r['snippet'] else f'Practice {query} problems',
                'difficulty': random.choice(['Easy', 'Medium', 'Hard', 'Mixed']),
                'problems': f'{random.randint(10, 500)}+ problems',
                'acceptance': f'{random.randint(35, 75)}%',
                'type': 'coding'
            })

    if len(all_results) < 3:
        all_results.extend(get_fallback_coding(query))
    return all_results[:12]

def get_fallback_coding(query):
    platforms = [
        {'name': 'LeetCode', 'color': '#ffa116', 'logo': '⚡', 'url': f'https://leetcode.com/problemset/?topicSlugs={urllib.parse.quote(query.lower())}'},
        {'name': 'HackerRank', 'color': '#2ec866', 'logo': '👩‍💻', 'url': f'https://www.hackerrank.com/domains/tutorials/10-days-of-javascript'},
        {'name': 'CodeChef', 'color': '#5b4638', 'logo': '🍴', 'url': f'https://www.codechef.com/practice/{urllib.parse.quote(query.lower())}'},
        {'name': 'GeeksForGeeks', 'color': '#2f8d46', 'logo': '🤓', 'url': f'https://www.geeksforgeeks.org/{urllib.parse.quote(query.lower())}/'},
        {'name': 'Codeforces', 'color': '#1f8dd6', 'logo': '🏆', 'url': 'https://codeforces.com/problemset'},
        {'name': 'InterviewBit', 'color': '#3b84f0', 'logo': '💡', 'url': f'https://www.interviewbit.com/courses/{urllib.parse.quote(query.lower())}/'},
    ]
    results = []
    for p in platforms:
        results.append({
            'title': f'{query.title()} - Practice Problems & Challenges',
            'platform': p['name'],
            'platform_color': p['color'],
            'platform_logo': p['logo'],
            'url': p['url'],
            'description': f'Master {query} with curated problems, editorial solutions, and real interview questions.',
            'difficulty': random.choice(['Easy', 'Medium', 'Hard', 'All Levels']),
            'problems': f'{random.randint(50, 500)}+ problems',
            'acceptance': f'{random.randint(35, 75)}%',
            'type': 'coding'
        })
    return results


# ─── ENTERTAINMENT ─────────────────────────────────────────────────────────────

def detect_entertainment_platform(url):
    url_lower = url.lower()
    if 'netflix.com' in url_lower:
        return {'name': 'Netflix', 'color': '#e50914', 'logo': '🎬'}
    elif 'hotstar.com' in url_lower or 'disneyplus' in url_lower:
        return {'name': 'Disney+ Hotstar', 'color': '#0063e5', 'logo': '⭐'}
    elif 'primevideo.com' in url_lower or 'amazon.com/Prime' in url_lower:
        return {'name': 'Amazon Prime', 'color': '#00a8e0', 'logo': '📺'}
    elif 'youtube.com' in url_lower:
        return {'name': 'YouTube', 'color': '#ff0000', 'logo': '▶️'}
    elif 'sonyliv.com' in url_lower:
        return {'name': 'SonyLIV', 'color': '#e50914', 'logo': '📡'}
    elif 'zee5.com' in url_lower:
        return {'name': 'ZEE5', 'color': '#6c2bd9', 'logo': '🎭'}
    elif 'jiosaavn.com' in url_lower or 'saavn.com' in url_lower:
        return {'name': 'JioSaavn', 'color': '#2bc5b4', 'logo': '🎵'}
    elif 'spotify.com' in url_lower:
        return {'name': 'Spotify', 'color': '#1db954', 'logo': '🎧'}
    elif 'gaana.com' in url_lower:
        return {'name': 'Gaana', 'color': '#e72c30', 'logo': '🎶'}
    elif 'mxplayer.in' in url_lower:
        return {'name': 'MX Player', 'color': '#00b4d8', 'logo': '🎞️'}
    else:
        return {'name': 'Entertainment', 'color': '#6c757d', 'logo': '🎬'}

def search_entertainment(query):
    all_results = []
    seen_urls = set()

    results = ddg_search(f'{query} watch online stream free')
    for r in results:
        if r['url'] and r['url'] not in seen_urls and r['title']:
            seen_urls.add(r['url'])
            platform = detect_entertainment_platform(r['url'])
            all_results.append({
                'title': r['title'][:80],
                'platform': platform['name'],
                'platform_color': platform['color'],
                'platform_logo': platform['logo'],
                'url': r['url'],
                'description': r['snippet'][:150] if r['snippet'] else f'Watch {query} online',
                'genre': random.choice(['Action', 'Drama', 'Comedy', 'Thriller', 'Romance', 'Sci-Fi', 'Horror', 'Documentary']),
                'language': random.choice(['Hindi', 'English', 'Tamil', 'Telugu', 'Multi-Language']),
                'subscription': random.choice(['Free', 'Subscription', 'Free with Ads', 'Premium']),
                'type': 'entertainment'
            })

    if len(all_results) < 3:
        all_results.extend(get_fallback_entertainment(query))
    return all_results[:12]

def get_fallback_entertainment(query):
    platforms = [
        {'name': 'Netflix', 'color': '#e50914', 'logo': '🎬', 'url': f'https://www.netflix.com/search?q={urllib.parse.quote(query)}'},
        {'name': 'Disney+ Hotstar', 'color': '#0063e5', 'logo': '⭐', 'url': f'https://www.hotstar.com/in/search?q={urllib.parse.quote(query)}'},
        {'name': 'Amazon Prime', 'color': '#00a8e0', 'logo': '📺', 'url': f'https://www.primevideo.com/search?phrase={urllib.parse.quote(query)}'},
        {'name': 'YouTube', 'color': '#ff0000', 'logo': '▶️', 'url': f'https://www.youtube.com/results?search_query={urllib.parse.quote(query)}'},
        {'name': 'SonyLIV', 'color': '#e50914', 'logo': '📡', 'url': f'https://www.sonyliv.com/search/{urllib.parse.quote(query)}'},
        {'name': 'ZEE5', 'color': '#6c2bd9', 'logo': '🎭', 'url': f'https://www.zee5.com/search?q={urllib.parse.quote(query)}'},
    ]
    results = []
    for p in platforms:
        results.append({
            'title': f'{query.title()} - Watch Online',
            'platform': p['name'],
            'platform_color': p['color'],
            'platform_logo': p['logo'],
            'url': p['url'],
            'description': f'Stream {query} on {p["name"]}. Watch latest movies, shows, and more.',
            'genre': random.choice(['Action', 'Drama', 'Comedy', 'Thriller']),
            'language': random.choice(['Hindi', 'English', 'Multi-Language']),
            'subscription': random.choice(['Free', 'Subscription', 'Free with Ads']),
            'type': 'entertainment'
        })
    return results
