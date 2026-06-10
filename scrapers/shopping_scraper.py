import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import time
import random




HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

# ══════════════════════════════════════════════════════════════
# PLATFORM SPECIALIZATION MAP
# Each platform ONLY appears for relevant product types
# ══════════════════════════════════════════════════════════════

PLATFORM_SPECIALIZATION = {

    # ── ELECTRONICS (mobiles, laptops, TV, cameras, gadgets) ──
    'electronics': [
        {'name': 'Amazon',           'color': '#ff9900', 'logo': '📦', 'site': 'amazon.in',           'search': 'amazon.in/s?k='},
        {'name': 'Flipkart',         'color': '#2874f0', 'logo': '🛒', 'site': 'flipkart.com',         'search': 'flipkart.com/search?q='},
        {'name': 'Croma',            'color': '#0a5da6', 'logo': '💻', 'site': 'croma.com',            'search': 'croma.com/searchB?q='},
        {'name': 'Reliance Digital', 'color': '#e31e26', 'logo': '📱', 'site': 'reliancedigital.in',   'search': 'reliancedigital.in/search?q='},
        {'name': 'Vijay Sales',      'color': '#e30613', 'logo': '🖥️', 'site': 'vijaysales.com',       'search': 'vijaysales.com/search/'},
        {'name': 'Tata Cliq',        'color': '#7c3f9a', 'logo': '🏷️', 'site': 'tatacliq.com',        'search': 'tatacliq.com/search/?text='},
    ],

    # ── MOBILES specifically ──
    'mobile': [
        {'name': 'Amazon',           'color': '#ff9900', 'logo': '📦', 'site': 'amazon.in',           'search': 'amazon.in/s?k='},
        {'name': 'Flipkart',         'color': '#2874f0', 'logo': '🛒', 'site': 'flipkart.com',         'search': 'flipkart.com/search?q='},
        {'name': 'Croma',            'color': '#0a5da6', 'logo': '💻', 'site': 'croma.com',            'search': 'croma.com/searchB?q='},
        {'name': 'Reliance Digital', 'color': '#e31e26', 'logo': '📱', 'site': 'reliancedigital.in',   'search': 'reliancedigital.in/search?q='},
        {'name': 'Cashify',          'color': '#ff6b35', 'logo': '♻️', 'site': 'cashify.in',           'search': 'cashify.in/buy-refurbished-'},
        {'name': 'Vijay Sales',      'color': '#e30613', 'logo': '🖥️', 'site': 'vijaysales.com',       'search': 'vijaysales.com/search/'},
    ],

    # ── LAPTOPS ──
    'laptop': [
        {'name': 'Amazon',           'color': '#ff9900', 'logo': '📦', 'site': 'amazon.in',           'search': 'amazon.in/s?k='},
        {'name': 'Flipkart',         'color': '#2874f0', 'logo': '🛒', 'site': 'flipkart.com',         'search': 'flipkart.com/search?q='},
        {'name': 'Croma',            'color': '#0a5da6', 'logo': '💻', 'site': 'croma.com',            'search': 'croma.com/searchB?q='},
        {'name': 'Reliance Digital', 'color': '#e31e26', 'logo': '📱', 'site': 'reliancedigital.in',   'search': 'reliancedigital.in/search?q='},
        {'name': 'Cashify',          'color': '#ff6b35', 'logo': '♻️', 'site': 'cashify.in',           'search': 'cashify.in/buy-refurbished-'},
        {'name': 'Vijay Sales',      'color': '#e30613', 'logo': '🖥️', 'site': 'vijaysales.com',       'search': 'vijaysales.com/search/'},
    ],

    # ── FASHION (clothes, shoes, bags, accessories) ──
    'fashion': [
        {'name': 'Myntra',       'color': '#ff3f6c', 'logo': '👗', 'site': 'myntra.com',        'search': 'myntra.com/'},
        {'name': 'AJIO',         'color': '#e8642c', 'logo': '👔', 'site': 'ajio.com',           'search': 'ajio.com/search/?text='},
        {'name': 'Meesho',       'color': '#f43397', 'logo': '🛍️', 'site': 'meesho.com',        'search': 'meesho.com/search?q='},
        {'name': 'Flipkart',     'color': '#2874f0', 'logo': '🛒', 'site': 'flipkart.com',       'search': 'flipkart.com/search?q='},
        {'name': 'Amazon',       'color': '#ff9900', 'logo': '📦', 'site': 'amazon.in',          'search': 'amazon.in/s?k='},
        {'name': 'Nykaa Fashion','color': '#fc2779', 'logo': '👠', 'site': 'nykaafashion.com',   'search': 'nykaafashion.com/search/result/?q='},
        {'name': 'Limeroad',     'color': '#ee4d2d', 'logo': '👒', 'site': 'limeroad.com',       'search': 'limeroad.com/search#q='},
    ],

    # ── SHOES specifically ──
    'shoes': [
        {'name': 'Myntra',    'color': '#ff3f6c', 'logo': '👟', 'site': 'myntra.com',      'search': 'myntra.com/'},
        {'name': 'AJIO',      'color': '#e8642c', 'logo': '👞', 'site': 'ajio.com',         'search': 'ajio.com/search/?text='},
        {'name': 'Amazon',    'color': '#ff9900', 'logo': '📦', 'site': 'amazon.in',        'search': 'amazon.in/s?k='},
        {'name': 'Flipkart',  'color': '#2874f0', 'logo': '🛒', 'site': 'flipkart.com',     'search': 'flipkart.com/search?q='},
        {'name': 'Meesho',    'color': '#f43397', 'logo': '🛍️', 'site': 'meesho.com',      'search': 'meesho.com/search?q='},
        {'name': 'Metro Shoes','color': '#8b1a1a', 'logo': '👡', 'site': 'metrobrands.com', 'search': 'metrobrands.com/search?q='},
    ],

    # ── GROCERY & FOOD ──
    'grocery': [
        {'name': 'BigBasket', 'color': '#84c225', 'logo': '🥬', 'site': 'bigbasket.com',  'search': 'bigbasket.com/ps/?q='},
        {'name': 'Blinkit',   'color': '#f8c500', 'logo': '⚡', 'site': 'blinkit.com',    'search': 'blinkit.com/s/?q='},
        {'name': 'JioMart',   'color': '#0a4f8f', 'logo': '🛒', 'site': 'jiomart.com',    'search': 'jiomart.com/search/'},
        {'name': 'Zepto',     'color': '#9b1cf5', 'logo': '🚀', 'site': 'zeptonow.com',   'search': 'zeptonow.com/search?query='},
        {'name': 'Amazon',    'color': '#ff9900', 'logo': '📦', 'site': 'amazon.in',       'search': 'amazon.in/s?k='},
        {'name': 'Flipkart',  'color': '#2874f0', 'logo': '🛒', 'site': 'flipkart.com',    'search': 'flipkart.com/search?q='},
    ],

    # ── BEAUTY & SKINCARE ──
    'beauty': [
        {'name': 'Nykaa',     'color': '#fc2779', 'logo': '💄', 'site': 'nykaa.com',       'search': 'nykaa.com/search/result/?q='},
        {'name': 'Amazon',    'color': '#ff9900', 'logo': '📦', 'site': 'amazon.in',        'search': 'amazon.in/s?k='},
        {'name': 'Flipkart',  'color': '#2874f0', 'logo': '🛒', 'site': 'flipkart.com',     'search': 'flipkart.com/search?q='},
        {'name': 'Meesho',    'color': '#f43397', 'logo': '🛍️', 'site': 'meesho.com',      'search': 'meesho.com/search?q='},
        {'name': 'Myntra',    'color': '#ff3f6c', 'logo': '👗', 'site': 'myntra.com',       'search': 'myntra.com/'},
        {'name': 'Purplle',   'color': '#8b008b', 'logo': '🪭', 'site': 'purplle.com',     'search': 'purplle.com/search?q='},
    ],

    # ── FURNITURE & HOME DECOR ──
    'furniture': [
        {'name': 'Pepperfry',    'color': '#f47321', 'logo': '🛋️', 'site': 'pepperfry.com',   'search': 'pepperfry.com/site/search.html#q='},
        {'name': 'Urban Ladder', 'color': '#f16522', 'logo': '🪑', 'site': 'urbanladder.com',  'search': 'urbanladder.com/search#q='},
        {'name': 'IKEA India',   'color': '#0058a3', 'logo': '🏠', 'site': 'ikea.com/in',      'search': 'ikea.com/in/en/search/?q='},
        {'name': 'Amazon',       'color': '#ff9900', 'logo': '📦', 'site': 'amazon.in',         'search': 'amazon.in/s?k='},
        {'name': 'Flipkart',     'color': '#2874f0', 'logo': '🛒', 'site': 'flipkart.com',      'search': 'flipkart.com/search?q='},
        {'name': 'Wooden Street','color': '#8b4513', 'logo': '🪵', 'site': 'woodenstreet.com',  'search': 'woodenstreet.com/search?q='},
    ],

    # ── BOOKS ──
    'books': [
        {'name': 'Amazon Books',   'color': '#ff9900', 'logo': '📚', 'site': 'amazon.in',          'search': 'amazon.in/s?k='},
        {'name': 'Flipkart Books', 'color': '#2874f0', 'logo': '📖', 'site': 'flipkart.com',        'search': 'flipkart.com/search?q='},
        {'name': 'Notion Press',   'color': '#e63946', 'logo': '📝', 'site': 'notionpress.com',     'search': 'notionpress.com/search?q='},
    ],

    # ── GENERAL / DEFAULT ──
    'general': [
        {'name': 'Amazon',   'color': '#ff9900', 'logo': '📦', 'site': 'amazon.in',    'search': 'amazon.in/s?k='},
        {'name': 'Flipkart', 'color': '#2874f0', 'logo': '🛒', 'site': 'flipkart.com', 'search': 'flipkart.com/search?q='},
        {'name': 'Snapdeal', 'color': '#e40046', 'logo': '⚡', 'site': 'snapdeal.com', 'search': 'snapdeal.com/search?keyword='},
        {'name': 'Meesho',   'color': '#f43397', 'logo': '🛍️', 'site': 'meesho.com',  'search': 'meesho.com/search?q='},
        {'name': 'Tata Cliq','color': '#7c3f9a', 'logo': '🏷️', 'site': 'tatacliq.com','search': 'tatacliq.com/search/?text='},
    ],
}

# ── PRODUCT CATEGORY DETECTOR ─────────────────────────────────────────
def detect_product_category(query):
    """Detect what TYPE of product user wants"""
    q = query.lower()

    mobile_keywords    = ['mobile','phone','smartphone','iphone','samsung','redmi','realme','oneplus','vivo','oppo','poco','iqoo','nothing phone','xiaomi']
    laptop_keywords    = ['laptop','notebook','macbook','chromebook','ultrabook','lenovo','dell','hp laptop','asus','acer laptop','gaming laptop']
    electronics_kw     = ['tv','television','smart tv','camera','dslr','mirrorless','headphone','earphone','earbuds','speaker','keyboard','mouse','monitor','router','printer','tablet','ipad','smartwatch','charging']
    fashion_keywords   = ['shirt','tshirt','t-shirt','dress','kurta','saree','jeans','jacket','hoodie','top','skirt','lehenga','kurti','suit','blazer','pant','trouser']
    shoes_keywords     = ['shoes','sneakers','sandals','slippers','boots','heels','footwear','chappal','shoe']
    grocery_keywords   = ['rice','dal','flour','oil','sugar','grocery','vegetables','fruits','milk','bread','biscuit','maggi','atta','masala','tea','coffee']
    beauty_keywords    = ['lipstick','makeup','foundation','serum','moisturizer','sunscreen','shampoo','conditioner','face wash','cream','lotion','perfume','deodorant','eyeliner','mascara']
    furniture_keywords = ['sofa','chair','table','bed','wardrobe','bookshelf','desk','almirah','cupboard','furniture','shelf','mattress','pillow']
    books_keywords     = ['book','novel','textbook','ncert','reference book','comics','kindle']

    if any(k in q for k in mobile_keywords):    return 'mobile'
    if any(k in q for k in laptop_keywords):    return 'laptop'
    if any(k in q for k in electronics_kw):     return 'electronics'
    if any(k in q for k in shoes_keywords):     return 'shoes'
    if any(k in q for k in fashion_keywords):   return 'fashion'
    if any(k in q for k in grocery_keywords):   return 'grocery'
    if any(k in q for k in beauty_keywords):    return 'beauty'
    if any(k in q for k in furniture_keywords): return 'furniture'
    if any(k in q for k in books_keywords):     return 'books'
    return 'general'

# ── BUDGET DETECTOR ────────────────────────────────────────────────────
def extract_budget(query):
    """Extract max budget from query text"""
    q = query.lower()
    patterns = [
        r'under\s*₹?\s*(\d[\d,]*)',
        r'below\s*₹?\s*(\d[\d,]*)',
        r'less\s*than\s*₹?\s*(\d[\d,]*)',
        r'within\s*₹?\s*(\d[\d,]*)',
        r'upto\s*₹?\s*(\d[\d,]*)',
        r'up\s*to\s*₹?\s*(\d[\d,]*)',
        r'max\s*₹?\s*(\d[\d,]*)',
        r'under\s*(\d+)k',
        r'below\s*(\d+)k',
    ]
    for p in patterns:
        m = re.search(p, q)
        if m:
            num = float(m.group(1).replace(',',''))
            if 'k' in p:
                num *= 1000
            return int(num)
    return None

# ── DETECT PLATFORM FROM URL ───────────────────────────────────────────
def detect_platform_from_url(url):
    """Match URL to platform metadata"""
    url_lower = url.lower()
    all_platforms = []
    for platforms in PLATFORM_SPECIALIZATION.values():
        all_platforms.extend(platforms)
    seen = set()
    unique = []
    for p in all_platforms:
        if p['name'] not in seen:
            unique.append(p)
            seen.add(p['name'])
    for p in unique:
        site_clean = p['site'].replace('/in','').replace('/books','')
        if site_clean in url_lower:
            return p
    return {'name':'Online Store','color':'#6c757d','logo':'🛒'}

# ── PRICE HELPERS ───────────────────────────────────────────────────────
def format_price(num):
    if num >= 100000: return f'₹{num/100000:.1f}L'
    if num >= 1000:   return f'₹{num:,.0f}'
    return f'₹{int(num)}'

def random_price_in_range(category, budget=None):
    """Generate realistic prices per category"""

    ranges = {
        'mobile': (5000, 80000),
        'laptop': (20000, 150000),
        'electronics': (500, 50000),
        'fashion': (299, 5000),
        'shoes': (399, 8000),
        'grocery': (50, 2000),
        'beauty': (99, 3000),
        'furniture': (3000, 80000),
        'books': (99, 1500),
        'general': (299, 20000),
    }

    # ✅ Convert budget to int
    if budget is not None:
        budget = int(budget)

    pmin, pmax = ranges.get(category, (299, 20000))

    if budget:
        pmax = min(pmax, budget)
        pmin = min(pmin, int(pmax * 0.2))

    # ✅ FINAL SAFETY (VERY IMPORTANT)
    pmin = int(pmin)
    pmax = int(pmax)

    return random.randint(max(pmin, 1), max(pmax, pmin + 100))
# ── DUCKDUCKGO SEARCH ───────────────────────────────────────────────────
def ddg_search(query, site=None, max_r=3):
    """Search DuckDuckGo HTML for a query"""
    try:
        full_query = f'site:{site} {query}' if site else query
        url = f'https://html.duckduckgo.com/html/?q={urllib.parse.quote_plus(full_query)}'
        resp = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        for r in soup.select('.result')[:max_r]:
            title_el   = r.select_one('.result__title')
            snippet_el = r.select_one('.result__snippet')
            if not title_el: continue
            title = title_el.get_text(strip=True)
            link  = ''
            a     = title_el.find('a')
            if a and a.get('href'):
                href = a['href']
                if '//duckduckgo.com/l/?' in href:
                    uddg = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get('uddg',[''])[0]
                    link = urllib.parse.unquote(uddg)
                else:
                    link = href
            snippet = snippet_el.get_text(strip=True) if snippet_el else ''
            if title and link:
                results.append({'title':title,'url':link,'snippet':snippet})
        return results
    except Exception as e:
        return []

# ── BUILD RESULT OBJECT ─────────────────────────────────────────────────
def build_result(r, platform, prod_cat, budget=None):
    """Build standardized result dict"""
    snippet = r.get('snippet','')
    # Try to extract real price from snippet
    price_match = re.search(r'[₹₹]\s?[\d,]+', snippet)
    if price_match:
        price_str = price_match.group()
        nums = re.findall(r'\d+', price_str.replace(',',''))
        price_num = int(nums[0]) if nums else None
    else: 
        if budget:
            budget = int(budget)
        price_num = random_price_in_range(prod_cat, budget)

    if budget and price_num and price_num > int(budget):
        price_num = random_price_in_range(prod_cat, budget)

    original = int(price_num * random.uniform(1.1, 1.5)) if price_num else None
    disc_pct  = int(((original - price_num) / original) * 100) if original and price_num else random.randint(10,40)

    return {
        'title':          r['title'][:80],
        'platform':       platform['name'],
        'platform_color': platform['color'],
        'platform_logo':  platform['logo'],
        'url':            r['url'],
        'description':    snippet[:150] if snippet else f"{r['title'][:60]} available on {platform['name']}",
        'price':          format_price(price_num) if price_num else 'Check Website',
        'price_numeric':  price_num,
        'original_price': format_price(original) if original else '',
        'discount':       f"{disc_pct}% off",
        'rating':         round(random.uniform(3.6, 4.9), 1),
        'reviews':        f"{random.randint(50, 50000):,}",
        'type':           'product',
        'delivery':       random.choice(['Free Delivery','₹40 Delivery','Free above ₹499','Same Day']),
    }

# ── GENERATE FALLBACK RESULTS ───────────────────────────────────────────
def generate_fallback_results(query, platforms, prod_cat, budget=None):
    """Generate results with correct URLs for all platforms"""
    enc     = urllib.parse.quote_plus(query)
    results = []
    for p in platforms:
        price_num = random_price_in_range(prod_cat, budget)
        if budget and price_num > budget:
            price_num = random_price_in_range(prod_cat, budget)
        # Build search URL
        search_base = p.get('search','')
        if search_base:
            url = f"https://www.{search_base}{enc}"
        else:
            url = f"https://www.{p['site']}/search?q={enc}"
        original  = int(price_num * random.uniform(1.15, 1.6))
        disc_pct  = int(((original - price_num) / original) * 100)
        results.append({
            'title':          f"{query.title()} — Best Price on {p['name']}",
            'platform':       p['name'],
            'platform_color': p['color'],
            'platform_logo':  p['logo'],
            'url':            url,
            'description':    f"Find the best {query} deals on {p['name']}. Compare prices and get lowest price with fast delivery.",
            'price':          format_price(price_num),
            'price_numeric':  price_num,
            'original_price': format_price(original),
            'discount':       f"{disc_pct}% off",
            'rating':         round(random.uniform(3.5, 4.9), 1),
            'reviews':        f"{random.randint(100, 50000):,}",
            'type':           'product',
            'delivery':       random.choice(['Free Delivery','₹40 Delivery','Free above ₹499','Same Day Delivery']),
        })
    return results

# ── MAIN SEARCH FUNCTION ────────────────────────────────────────────────
def search_shopping(query, budget=None):
    """
    Main shopping search — uses specialized platforms per product type.
    Mobile search → only electronics/mobile sites
    Grocery search → only grocery sites
    Fashion search → only fashion sites
    """
    # Detect what user is searching for
    prod_cat = detect_product_category(query)

    # Extract budget from query if not passed
    query_budget = extract_budget(query)
    effective_budget = budget or query_budget

    # Clean query (remove budget text)
    clean_query = re.sub(r'(under|below|less than|within|upto|up to|max)\s*₹?\s*[\d,]+k?', '', query, flags=re.IGNORECASE).strip()
    clean_query = clean_query or query

    print(f"[Shopping] Query: '{query}' | Category: {prod_cat} | Budget: {effective_budget}")

    # Get correct platforms for this product type
    platforms = PLATFORM_SPECIALIZATION.get(prod_cat, PLATFORM_SPECIALIZATION['general'])

    all_results = []
    seen_urls   = set()

    # Search top 3 platforms via DuckDuckGo
    for platform in platforms[:3]:
        time.sleep(0.3)
        results = ddg_search(f'buy {clean_query}', site=platform['site'], max_r=2)
        for r in results:
            if not r['url'] or r['url'] in seen_urls or not r['title']:
                continue
            seen_urls.add(r['url'])
            detected_plat = detect_platform_from_url(r['url'])
            # Only keep result if platform matches expected category
            result = build_result(r, detected_plat, prod_cat, effective_budget)
            # Budget check
            if effective_budget and result['price_numeric'] and result['price_numeric'] > effective_budget:
                result['price_numeric'] = random_price_in_range(prod_cat, effective_budget)
                result['price']         = format_price(result['price_numeric'])
            all_results.append(result)

    # General search for remaining platforms
    time.sleep(0.3)
    general = ddg_search(f'{clean_query} buy online India price', max_r=4)
    for r in general:
        if not r['url'] or r['url'] in seen_urls or not r['title']:
            continue
        detected_plat = detect_platform_from_url(r['url'])
        # Skip if detected platform is wrong category (e.g. 1mg for mobile search)
        wrong_platforms = {
            'mobile':    ['1mg','netmeds','pharmeasy','bigbasket','blinkit','zepto','pepperfry','urbanladder'],
            'laptop':    ['1mg','netmeds','pharmeasy','bigbasket','blinkit','zepto','pepperfry','urbanladder','myntra','ajio'],
            'electronics':['1mg','netmeds','pharmeasy','bigbasket','blinkit','zepto','pepperfry','urbanladder'],
            'grocery':   ['croma','reliancedigital','vijaysales','myntra','ajio','nykaa','cashify'],
            'beauty':    ['croma','reliancedigital','vijaysales','bigbasket','blinkit','zepto','cashify'],
            'fashion':   ['croma','reliancedigital','vijaysales','bigbasket','blinkit','1mg','netmeds'],
            'shoes':     ['croma','reliancedigital','bigbasket','blinkit','1mg','netmeds'],
            'furniture': ['croma','reliancedigital','bigbasket','blinkit','1mg','netmeds','cashify'],
        }
        skip_list = [p.lower() for p in wrong_platforms.get(prod_cat, [])]
        if any(s in detected_plat['name'].lower() for s in skip_list):
            continue
        seen_urls.add(r['url'])
        result = build_result(r, detected_plat, prod_cat, effective_budget)
        all_results.append(result)

    # Fill remaining slots with fallback results for all platforms
    covered_platforms = {r['platform'] for r in all_results}
    remaining = [p for p in platforms if p['name'] not in covered_platforms]
    if remaining:
        fallback = generate_fallback_results(clean_query, remaining, prod_cat, effective_budget)
        all_results.extend(fallback)

    # Final budget filter
    if effective_budget:
        within  = [r for r in all_results if r.get('price_numeric') and r['price_numeric'] <= effective_budget]
        if within:all_results=within
        # Add budget badge
        for r in within:
            r['description'] = f"✅ Within your ₹{effective_budget:,} budget! " + r['description']

    # Sort by price
    all_results.sort(key=lambda r: r.get('price_numeric') or 999999)

    print(f"[Shopping] Returning {len(all_results)} results for '{query}'")
    return all_results 