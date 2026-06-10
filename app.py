from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import (
    init_db, register_user, login_user,
    get_all_users, get_total_users, get_todays_logins,
    get_all_login_logs, log_login,
    create_reset_token, reset_password, cleanup_expired_tokens
)
from scrapers.ai_assistant import (
    ai_search_courses, ai_search_jobs, ai_search_shopping,
    ai_search_scholarships, ai_search_coding, ai_search_entertainment,
    ai_career_roadmap, ai_chat, is_api_configured
)
import re,traceback

# Try to load scraper fallbacks
try:
    from scrapers.courses_scraper       import search_courses       as scrape_courses
    from scrapers.jobs_scraper          import search_jobs           as scrape_jobs
    from scrapers.shopping_scraper      import search_shopping       as scrape_shopping
    from scrapers.scholarships_scraper  import search_scholarships   as scrape_scholarships
    from scrapers.coding_scraper        import search_coding         as scrape_coding
    from scrapers.entertainment_scraper import search_entertainment  as scrape_entertainment
    from scrapers.roadmap_generator     import generate_roadmap      as scrape_roadmap
    SCRAPERS_OK = True
    print("✅ Scraper fallbacks loaded")
except Exception as e:
    print(f"⚠️  Scraper fallbacks not available: {e}")
    SCRAPERS_OK = False

app = Flask(__name__)
app.secret_key = 'nexussearch_super_secret_2024'
init_db()

# ── AUTH ──────────────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name','').strip()
        email = request.form.get('email','').strip()
        pwd   = request.form.get('password','').strip()
        if not name or not email or not pwd:
            return render_template('register.html', error='All fields required.')
        result = register_user(name, email, pwd)
        if result == 'exists':
            return render_template('register.html', error='Email already registered.')
        elif result == 'success':
            return render_template('login.html', success='Registered! Please login.')
        return render_template('register.html', error='Registration failed.')
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email','').strip()
        pwd   = request.form.get('password','').strip()
        user  = login_user(email, pwd)
        if user:
            session['user_id']    = user['id']
            session['user_name']  = user['name']
            session['user_email'] = user['email']
            log_login(user['id'], 'success')
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid email or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    name = session.get('user_name','User')
    session.clear()
    return render_template('logout.html', user_name=name)

@app.route('/forgot-password', methods=['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email','').strip().lower()
        token = create_reset_token(email)
        if token:
            return render_template('forgot_password.html', token=token, email=email)
        return render_template('forgot_password.html', error='Email not found.')
    return render_template('forgot_password.html')

@app.route('/reset-password', methods=['GET','POST'])
def reset_password_route():
    if request.method == 'GET':
        return render_template('reset_password.html', token=request.args.get('token',''))
    token    = request.form.get('token','').strip()
    new_pass = request.form.get('new_password','').strip()
    confirm  = request.form.get('confirm_password','').strip()
    if len(new_pass) < 6:
        return render_template('reset_password.html', error='Password must be 6+ chars.', token=token)
    if new_pass != confirm:
        return render_template('reset_password.html', error='Passwords do not match.', token=token)
    result = reset_password(token, new_pass)
    if result == 'success': return render_template('reset_password.html', success=True)
    if result == 'expired': return render_template('reset_password.html', warning='Token expired.', token='')
    return render_template('reset_password.html', error='Invalid token.', token=token)

# ── PAGES ─────────────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('index'))
    return render_template('dashboard.html',
        user_name=session.get('user_name'), ai_ready=is_api_configured())

@app.route('/roadmap')
def roadmap():
    if 'user_id' not in session: return redirect(url_for('index'))
    return render_template('roadmap.html',
        user_name=session.get('user_name'), ai_ready=is_api_configured())

@app.route('/compare')
def compare():
    if 'user_id' not in session: return redirect(url_for('index'))
    return render_template('compare.html', user_name=session.get('user_name'))

@app.route('/category/<cat_name>')
def category(cat_name):
    if 'user_id' not in session: return redirect(url_for('index'))
    cats = {
        'courses':       {'title':'Online Courses',   'icon':'🎓','color':'#ff6a00','desc':'AI-powered search across Udemy, Coursera, edX, YouTube & more'},
        'jobs':          {'title':'Job Portal',        'icon':'💼','color':'#cc2200','desc':'AI finds jobs from LinkedIn, Naukri, company career pages & more'},
        'shopping':      {'title':'Smart Shopping',    'icon':'🛒','color':'#ff9c40','desc':'AI compares prices across Amazon, Flipkart, Myntra & 30+ platforms'},
        'scholarships':  {'title':'Scholarships',      'icon':'🏆','color':'#ff7700','desc':'AI finds scholarships from NSP India, Buddy4Study, AICTE & more'},
        'coding':        {'title':'Coding Practice',   'icon':'💻','color':'#ff4400','desc':'AI finds resources from LeetCode, HackerRank, CodeChef & more'},
        'entertainment': {'title':'Entertainment',     'icon':'🎬','color':'#e03000','desc':'AI finds content on Netflix, Hotstar, Amazon Prime & more'},
    }
    cat_info = cats.get(cat_name, {'title':'Search','icon':'🔍','color':'#ff6a00','desc':''})
    return render_template('category.html',
        cat_name=cat_name, cat_info=cat_info,
        user_name=session.get('user_name'), ai_ready=is_api_configured())

# ══════════════════════════════════════════════════════════════
# MAIN SEARCH ROUTE — AI POWERED
# ══════════════════════════════════════════════════════════════
@app.route('/search', methods=['POST'])
def search():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    data     = request.get_json()
    query    = data.get('query','').strip()
    category = data.get('category','').lower()
    budget   = data.get('budget', None)

    if not query:
        return jsonify({'error': 'Please enter a search query'}), 400

    print(f"\n{'='*50}")
    print(f"🔍 Search: '{query}' | Category: {category} | Budget: {budget}")
    print(f"🤖 AI Ready: {is_api_configured()}")

    results = []
    ai_used = False
    error_msg = None

    # ── AI SEARCH ────────────────────────────────────────────
    if is_api_configured():
        try:
            bgt = float(budget) if budget else None
            if   category == 'courses':       results = ai_search_courses(query) or []
            elif category == 'jobs':          results = ai_search_jobs(query) or []
            elif category == 'shopping':      results = ai_search_shopping(query, budget=bgt) or []
            elif category == 'scholarships':  results = ai_search_scholarships(query) or []
            elif category == 'coding':        results = ai_search_coding(query) or []
            elif category == 'entertainment': results = ai_search_entertainment(query) or []

            if results:
                ai_used = True
                print(f"✅ AI returned {len(results)} results")
            else:
                print(f"⚠️  AI returned 0 results — trying scraper fallback")
        except Exception as e:
            print(f"❌ AI error: {e}")
            traceback.print_exc()
            error_msg = str(e)

    # ── SCRAPER FALLBACK ──────────────────────────────────────
    if not results and SCRAPERS_OK:
        print(f"🔄 Using scraper fallback...")
        try:
            bgt = float(budget) if budget else None
            if   category == 'courses':       results = scrape_courses(query) or []
            elif category == 'jobs':          results = scrape_jobs(query) or []
            elif category == 'shopping':      results = scrape_shopping(query, budget=bgt) or []
            elif category == 'scholarships':  results = scrape_scholarships(query) or []
            elif category == 'coding':        results = scrape_coding(query) or []
            elif category == 'entertainment': results = scrape_entertainment(query) or []
            print(f"✅ Scraper returned {len(results)} results")
        except Exception as e:
            print(f"❌ Scraper error: {e}")

    print(f"📊 Final: {len(results)} results | AI: {ai_used}")
    print(f"{'='*50}\n")

    return jsonify({
        'results':  results,
        'query':    query,
        'category': category,
        'ai_used':  ai_used,
        'count':    len(results),
        'error':    error_msg
    })

# ── AI CHAT ────────────────────────────────────────────────────
@app.route('/api/ai-chat', methods=['POST'])
def api_ai_chat():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    data    = request.get_json()
    message = data.get('message','').strip()
    history = data.get('history', [])
    if not message:
        return jsonify({'error': 'Please enter a message'}), 400
    response = ai_chat(message, history)
    return jsonify({'response': response, 'ai_ready': is_api_configured()})

@app.route('/api/ai-status')
def api_ai_status():
    return jsonify({'ai_ready': is_api_configured()})

# ── ROADMAP API ─────────────────────────────────────────────────
@app.route('/api/roadmap', methods=['POST'])
def api_roadmap():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    data  = request.get_json()
    goal  = data.get('goal','').strip()
    level = data.get('level','beginner')
    if not goal:
        return jsonify({'error': 'Please enter a career goal'}), 400

    if is_api_configured():
        rm = ai_career_roadmap(goal, level)
        if rm:
            return jsonify({'roadmap': rm, 'goal': goal, 'ai_powered': True})

    if SCRAPERS_OK:
        try:
            rm = scrape_roadmap(goal, level)
            return jsonify({'roadmap': rm, 'goal': goal, 'ai_powered': False})
        except: pass

    return jsonify({'error': 'Could not generate roadmap. Check API key.'}), 500

# ── COMPARE API ──────────────────────────────────────────────────
@app.route('/api/compare', methods=['POST'])
def api_compare():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    data     = request.get_json()
    query    = data.get('query','').strip()
    category = data.get('category','courses')
    if not query:
        return jsonify({'error': 'Enter a search term'}), 400
    results = []
    if is_api_configured():
        if   category == 'courses':  results = ai_search_courses(query) or []
        elif category == 'jobs':     results = ai_search_jobs(query) or []
        elif category == 'shopping': results = ai_search_shopping(query) or []
    elif SCRAPERS_OK:
        try:
            if   category == 'courses':  results = scrape_courses(query) or []
            elif category == 'jobs':     results = scrape_jobs(query) or []
            elif category == 'shopping': results = scrape_shopping(query) or []
        except: pass
    return jsonify({'results': results[:4], 'query': query})

# ── ADMIN ─────────────────────────────────────────────────────────
@app.route('/admin')
def admin():
    if request.args.get('key','') != 'nexusadmin2024':
        return '''<div style="font-family:Arial;text-align:center;padding:80px;background:#0a0500;min-height:100vh;color:#f5e6d8">
            <div style="font-size:56px">🔐</div>
            <h2 style="color:#ff6a00;margin:14px 0">Access Denied</h2>
            <p style="color:#8a6a50">Add <code style="color:#ff6a00">?key=nexusadmin2024</code> to URL</p>
            <a href="/" style="display:inline-block;margin-top:20px;padding:10px 24px;background:#ff6a00;color:#fff;text-decoration:none;border-radius:8px">← Login</a>
        </div>'''
    cleanup_expired_tokens()
    return render_template('admin.html',
        all_users=get_all_users(), total_users=get_total_users(),
        login_logs=get_all_login_logs(), todays_logins=get_todays_logins())

if __name__ == '__main__':
    print("\n" + "="*55)
    print("🔥  NexusSearch Starting...")
    ai_ok = is_api_configured()
    print(f"🤖  AI Status  : {'✅ READY' if ai_ok else '❌ API KEY NOT SET'}")
    print(f"🔄  Scrapers   : {'✅ Available' if SCRAPERS_OK else '⚠️  Not loaded'}")
    if not ai_ok:
        print("👉  Add your key in scrapers/ai_assistant.py line 20")
    print("="*55 + "\n")
    app.run(debug=True, port=5000, threaded=True)