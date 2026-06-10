# 🔮 NexusSearch — Unified Digital Intelligence Hub

## 🚀 What This App Does
NexusSearch automatically searches **50+ platforms** across 6 categories when you type a single query:

| Category | Platforms Searched |
|----------|-------------------|
| 🎓 Courses | Udemy, Coursera, edX, YouTube, Khan Academy, Skillshare |
| 💼 Jobs | LinkedIn, Indeed, Naukri, Glassdoor, Internshala, Wellfound |
| 🛒 Shopping | Amazon, Flipkart, Myntra, Meesho, Snapdeal, Croma |
| 🏆 Scholarships | NSP India, Buddy4Study, AICTE, Vidyasaarathi, PFMS |
| 💻 Coding | LeetCode, HackerRank, CodeChef, Codeforces, GeeksForGeeks |
| 🎬 Entertainment | Netflix, Disney+Hotstar, Amazon Prime, YouTube, SonyLIV, ZEE5 |

## ✨ Features
- 🔐 **Login/Registration** — with duplicate email detection
- 🎨 **Beautiful Dashboard** — animated hero slider + category cards
- 🔍 **Smart Search** — auto-searches all platforms in each category
- 📊 **Visual Charts** — pie chart (platform distribution) + bar chart (ratings)
- 📋 **Results Cards** — with platform, price, rating, metadata
- 🌐 **Real Web Scraping** — using DuckDuckGo search + BeautifulSoup
- 👋 **Animated Logout** — beautiful goodbye page with countdown

## 🛠️ Setup & Run (VSCode)

### Step 1 — Open in VSCode
```
Open the NexusSearch folder in VSCode
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run the App
```bash
python app.py
```

### Step 5 — Open Browser
```
http://localhost:5000
```

## 📁 Project Structure
```
NexusSearch/
├── app.py                      # Main Flask application
├── database.py                 # SQLite user auth & DB
├── requirements.txt            # Python dependencies
├── nexussearch.db              # Auto-created SQLite DB
├── scrapers/
│   ├── __init__.py
│   ├── courses_scraper.py      # Udemy, Coursera, edX...
│   ├── jobs_scraper.py         # LinkedIn, Indeed, Naukri...
│   ├── shopping_scraper.py     # Amazon, Flipkart, Myntra...
│   ├── scholarships_scraper.py # NSP, Buddy4Study, AICTE...
│   ├── coding_scraper.py       # LeetCode, HackerRank...
│   └── entertainment_scraper.py # Netflix, Hotstar, Prime...
└── templates/
    ├── login.html              # Login page
    ├── register.html           # Registration page
    ├── dashboard.html          # Main dashboard with slider
    ├── category.html           # Search + results + charts
    └── logout.html             # Goodbye page
```

## 💡 How It Works
1. User logs in / registers
2. Dashboard shows 6 category cards with animated slider
3. User clicks a category (e.g., Courses)
4. User types query (e.g., "Python programming under budget")
5. App automatically searches DuckDuckGo with site-specific queries for each platform
6. Results displayed in cards with metadata + price/salary/rating
7. Charts auto-generated: Platform Distribution (pie) + Ratings (bar)

## 🔧 Customization
- Add more platforms in each `scrapers/*.py` file
- Modify UI colors in CSS `:root` variables
- Add more categories in `app.py` category dict
- Enable Selenium for deeper scraping (install `selenium` + ChromeDriver)

## 🔒 Tech Stack
- **Backend**: Python 3.8+ / Flask
- **Database**: SQLite (auto-created)
- **Scraping**: requests + BeautifulSoup + DuckDuckGo HTML
- **Frontend**: HTML5 / CSS3 / Vanilla JS
- **Charts**: Chart.js (CDN)
- **Fonts**: Google Fonts (Orbitron, Rajdhani, Inter)

---
Built with ❤️ — NexusSearch v1.0
