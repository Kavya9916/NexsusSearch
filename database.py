import sqlite3
import hashlib
import secrets
import string
from datetime import datetime, timedelta

DB_PATH = 'nexussearch.db'

# ── DATABASE CONNECTION ────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ── INITIALIZE ALL TABLES ──────────────────────────────────────────────────────
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            email       TEXT    UNIQUE NOT NULL,
            password    TEXT    NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Search history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            query       TEXT,
            category    TEXT,
            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # 3. Login logs table
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_logs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER,
                login_time  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status      TEXT DEFAULT 'success',
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
    except Exception as e:
        print(f"login_logs table note: {e}")

    # 4. Active sessions table
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_sessions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER,
                login_time  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
    except Exception as e:
        print(f"active_sessions table note: {e}")

    # 5. Password reset tokens table (NEW — for forgot password)
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS password_resets (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                email       TEXT    NOT NULL,
                token       TEXT    NOT NULL UNIQUE,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at  TIMESTAMP NOT NULL,
                used        INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
    except Exception as e:
        print(f"password_resets table note: {e}")

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

# ── PASSWORD HELPERS ───────────────────────────────────────────────────────────
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(length=32):
    """Generate a secure random token for password reset"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# ── USER REGISTRATION ──────────────────────────────────────────────────────────
def register_user(name, email, password):
    """
    Register a new user.
    Returns: 'exists' | 'success' | 'error'
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        # Check if email already exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        existing = cursor.fetchone()
        if existing:
            return 'exists'
        # Hash password and save
        hashed = hash_password(password)
        cursor.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, hashed)
        )
        conn.commit()
        return 'success'
    except Exception as e:
        print(f"Register error: {e}")
        return 'error'
    finally:
        conn.close()

# ── USER LOGIN ─────────────────────────────────────────────────────────────────
def login_user(email, password):
    """
    Verify login credentials.
    Returns: user dict if valid, None if invalid
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        hashed = hash_password(password)
        cursor.execute(
            'SELECT * FROM users WHERE email = ? AND password = ?',
            (email, hashed)
        )
        user = cursor.fetchone()
        if user:
            return dict(user)
        return None
    except Exception as e:
        print(f"Login error: {e}")
        return None
    finally:
        conn.close()

# ── GET USER ───────────────────────────────────────────────────────────────────
def get_user(user_id):
    """Get user by ID"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None
    except Exception as e:
        print(f"Get user error: {e}")
        return None
    finally:
        conn.close()

def get_user_by_email(email):
    """Get user by email address"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        return dict(user) if user else None
    except Exception as e:
        print(f"Get user by email error: {e}")
        return None
    finally:
        conn.close()

# ── LOGIN LOGGING ──────────────────────────────────────────────────────────────
def log_login(user_id, status='success'):
    """Record every login attempt with timestamp"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO login_logs (user_id, login_time, status) VALUES (?, CURRENT_TIMESTAMP, ?)',
            (user_id, status)
        )
        conn.commit()
    except Exception as e:
        print(f"Log login error: {e}")
    finally:
        conn.close()

# ── ADMIN DATA FUNCTIONS ───────────────────────────────────────────────────────
def get_all_users():
    """Get all registered users ordered by newest first"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, name, email, created_at FROM users ORDER BY created_at DESC'
        )
        users = cursor.fetchall()
        return [dict(u) for u in users]
    except Exception as e:
        print(f"Get all users error: {e}")
        return []
    finally:
        conn.close()

def get_total_users():
    """Count total registered users"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM users')
        result = cursor.fetchone()
        return result['count']
    except Exception as e:
        print(f"Total users error: {e}")
        return 0
    finally:
        conn.close()

def get_todays_logins():
    """Count logins that happened today"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) as count FROM login_logs
            WHERE DATE(login_time) = DATE('now')
        ''')
        result = cursor.fetchone()
        return result['count']
    except Exception as e:
        print(f"Today logins error: {e}")
        return 0
    finally:
        conn.close()

def get_all_login_logs():
    """Get last 50 login records with user details"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                u.name,
                u.email,
                l.login_time,
                l.status,
                l.id as log_id
            FROM login_logs l
            JOIN users u ON l.user_id = u.id
            ORDER BY l.login_time DESC
            LIMIT 50
        ''')
        logs = cursor.fetchall()
        return [dict(l) for l in logs]
    except Exception as e:
        print(f"Login logs error: {e}")
        return []
    finally:
        conn.close()

def get_login_stats():
    """Get login statistics for charts"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        # Last 7 days login count per day
        cursor.execute('''
            SELECT
                DATE(login_time) as day,
                COUNT(*) as count
            FROM login_logs
            WHERE login_time >= DATE('now', '-7 days')
            GROUP BY DATE(login_time)
            ORDER BY day ASC
        ''')
        daily = cursor.fetchall()
        return [dict(d) for d in daily]
    except Exception as e:
        print(f"Login stats error: {e}")
        return []
    finally:
        conn.close()

# ── SEARCH HISTORY ─────────────────────────────────────────────────────────────
def save_search(user_id, query, category):
    """Save user search to history"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO search_history (user_id, query, category) VALUES (?, ?, ?)',
            (user_id, query, category)
        )
        conn.commit()
    except Exception as e:
        print(f"Save search error: {e}")
    finally:
        conn.close()

# ══════════════════════════════════════════════════════════════════════════════
# FORGOT PASSWORD FEATURE
# ══════════════════════════════════════════════════════════════════════════════

def create_reset_token(email):
    """
    Create a password reset token for the given email.
    Returns: token string if email exists, None if email not found
    """
    conn = get_db()
    try:
        cursor = conn.cursor()

        # Check if email exists in users table
        cursor.execute('SELECT id, name, email FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if not user:
            return None  # Email not registered

        user = dict(user)

        # Delete any existing unused tokens for this email
        cursor.execute(
            'DELETE FROM password_resets WHERE email = ? AND used = 0',
            (email,)
        )

        # Generate new secure token
        token = generate_token(32)

        # Token expires in 30 minutes
        expires_at = datetime.now() + timedelta(minutes=30)

        # Save token to database
        cursor.execute('''
            INSERT INTO password_resets (user_id, email, token, expires_at, used)
            VALUES (?, ?, ?, ?, 0)
        ''', (user['id'], email, token, expires_at.strftime('%Y-%m-%d %H:%M:%S')))

        conn.commit()
        return token

    except Exception as e:
        print(f"Create reset token error: {e}")
        return None
    finally:
        conn.close()

def verify_reset_token(token):
    """
    Verify if a password reset token is valid, not expired, and not used.
    Returns: user dict if valid, None if invalid/expired
    """
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT pr.*, u.name, u.email as user_email
            FROM password_resets pr
            JOIN users u ON pr.user_id = u.id
            WHERE pr.token = ?
              AND pr.used = 0
              AND pr.expires_at > CURRENT_TIMESTAMP
        ''', (token,))
        reset = cursor.fetchone()
        if reset:
            return dict(reset)
        return None
    except Exception as e:
        print(f"Verify token error: {e}")
        return None
    finally:
        conn.close()

def reset_password(token, new_password):
    """
    Reset user password using a valid token.
    Returns: 'success' | 'invalid' | 'expired' | 'error'
    """
    conn = get_db()
    try:
        cursor = conn.cursor()

        # Check token exists and is valid
        cursor.execute('''
            SELECT * FROM password_resets
            WHERE token = ? AND used = 0
        ''', (token,))
        reset = cursor.fetchone()

        if not reset:
            return 'invalid'

        reset = dict(reset)

        # Check if expired
        expires_at = datetime.strptime(reset['expires_at'], '%Y-%m-%d %H:%M:%S')
        if datetime.now() > expires_at:
            return 'expired'

        # Hash new password
        new_hashed = hash_password(new_password)

        # Update user password
        cursor.execute(
            'UPDATE users SET password = ? WHERE id = ?',
            (new_hashed, reset['user_id'])
        )

        # Mark token as used
        cursor.execute(
            'UPDATE password_resets SET used = 1 WHERE token = ?',
            (token,)
        )

        conn.commit()
        return 'success'

    except Exception as e:
        print(f"Reset password error: {e}")
        return 'error'
    finally:
        conn.close()

def cleanup_expired_tokens():
    """Delete all expired reset tokens — call this periodically"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM password_resets WHERE expires_at < CURRENT_TIMESTAMP'
        )
        conn.commit()
    except Exception as e:
        print(f"Cleanup tokens error: {e}")
    finally:
        conn.close()

# ── VIEW DATA IN TERMINAL (for VSCode) ────────────────────────────────────────
def print_all_data():
    """
    Print all database data in terminal.
    Run: python database.py
    """
    conn = get_db()
    cursor = conn.cursor()

    print("\n" + "="*65)
    print("🔥  NEXUSSEARCH DATABASE VIEWER")
    print("="*65)

    # ── USERS ──────────────────────────────────────────────────
    print("\n👥  ALL REGISTERED USERS")
    print("-"*65)
    cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
    users = cursor.fetchall()
    if users:
        print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Registered':<20}")
        print("-"*65)
        for u in users:
            print(f"{u['id']:<5} {u['name']:<20} {u['email']:<30} {u['created_at']:<20}")
    else:
        print("  No users registered yet!")

    # ── LOGIN LOGS ─────────────────────────────────────────────
    print("\n\n🔑  LOGIN HISTORY (Last 20)")
    print("-"*65)
    try:
        cursor.execute('''
            SELECT u.name, u.email, l.login_time, l.status
            FROM login_logs l
            JOIN users u ON l.user_id = u.id
            ORDER BY l.login_time DESC
            LIMIT 20
        ''')
        logs = cursor.fetchall()
        if logs:
            print(f"{'Name':<20} {'Email':<25} {'Time':<22} {'Status':<10}")
            print("-"*65)
            for l in logs:
                status = "✅ Success" if l['status'] == 'success' else "❌ Failed"
                print(f"{l['name']:<20} {l['email']:<25} {l['login_time']:<22} {status}")
        else:
            print("  No login history yet!")
    except Exception as e:
        print(f"  login_logs table not found: {e}")

    # ── PASSWORD RESETS ─────────────────────────────────────────
    print("\n\n🔐  PASSWORD RESET REQUESTS")
    print("-"*65)
    try:
        cursor.execute('''
            SELECT u.name, pr.email, pr.created_at, pr.expires_at, pr.used
            FROM password_resets pr
            JOIN users u ON pr.user_id = u.id
            ORDER BY pr.created_at DESC
            LIMIT 10
        ''')
        resets = cursor.fetchall()
        if resets:
            print(f"{'Name':<20} {'Email':<25} {'Requested':<20} {'Used':<8}")
            print("-"*65)
            for r in resets:
                used = "Yes" if r['used'] else "No"
                print(f"{r['name']:<20} {r['email']:<25} {r['created_at']:<20} {used:<8}")
        else:
            print("  No password reset requests yet!")
    except Exception as e:
        print(f"  password_resets table not found: {e}")

    # ── STATS ────────────────────────────────────────────────────
    print("\n\n📊  SUMMARY STATISTICS")
    print("-"*65)
    cursor.execute('SELECT COUNT(*) as c FROM users')
    total_users = cursor.fetchone()['c']
    print(f"  Total Registered Users  : {total_users}")

    try:
        cursor.execute("SELECT COUNT(*) as c FROM login_logs WHERE DATE(login_time) = DATE('now')")
        today = cursor.fetchone()['c']
        cursor.execute("SELECT COUNT(*) as c FROM login_logs")
        total_logins = cursor.fetchone()['c']
        print(f"  Logins Today            : {today}")
        print(f"  Total Logins Ever       : {total_logins}")
    except:
        print("  Login logs not available")

    try:
        cursor.execute("SELECT COUNT(*) as c FROM password_resets WHERE used = 0")
        pending = cursor.fetchone()['c']
        print(f"  Pending Reset Requests  : {pending}")
    except:
        pass

    print("\n" + "="*65)
    print("  Database file: nexussearch.db")
    print("  Run this anytime: python database.py")
    print("="*65 + "\n")

    conn.close()

# ── RUN DIRECTLY TO VIEW DATA ──────────────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    print_all_data()