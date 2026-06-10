import urllib.parse
import random

# Career roadmap templates - each maps a career goal to a structured path
ROADMAP_TEMPLATES = {
    'data scientist': {
        'title': 'Data Scientist',
        'emoji': '📊',
        'duration': '8–12 months',
        'phases': [
            {
                'phase': 1, 'title': 'Mathematics & Statistics Foundation',
                'duration': '4–6 weeks', 'color': '#ff6a00',
                'skills': ['Linear Algebra', 'Statistics', 'Probability', 'Calculus Basics'],
                'courses': [
                    {'name': 'Statistics for Data Science', 'platform': 'Coursera', 'url': 'https://www.coursera.org/learn/statistics-for-data-science-python', 'price': 'Free Audit', 'rating': 4.6},
                    {'name': 'Khan Academy Statistics', 'platform': 'Khan Academy', 'url': 'https://www.khanacademy.org/math/statistics-probability', 'price': 'Free', 'rating': 4.8},
                    {'name': 'Math for ML', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/mathematics-machine-learning', 'price': 'Free Audit', 'rating': 4.5},
                ],
                'practice': [
                    {'name': 'Statistics Problems', 'platform': 'HackerRank', 'url': 'https://www.hackerrank.com/domains/mathematics'},
                ],
            },
            {
                'phase': 2, 'title': 'Python Programming',
                'duration': '4–6 weeks', 'color': '#cc2200',
                'skills': ['Python Basics', 'NumPy', 'Pandas', 'Matplotlib', 'Data Wrangling'],
                'courses': [
                    {'name': 'Python for Everybody', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/python', 'price': 'Free Audit', 'rating': 4.8},
                    {'name': 'Python Bootcamp 2024', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/complete-python-bootcamp/', 'price': '₹499', 'rating': 4.7},
                    {'name': 'Intro to Python', 'platform': 'edX', 'url': 'https://www.edx.org/learn/python', 'price': 'Free', 'rating': 4.5},
                ],
                'practice': [
                    {'name': 'Python Challenges', 'platform': 'HackerRank', 'url': 'https://www.hackerrank.com/domains/python'},
                    {'name': 'Python Practice', 'platform': 'LeetCode', 'url': 'https://leetcode.com/problemset/'},
                ],
            },
            {
                'phase': 3, 'title': 'Machine Learning',
                'duration': '6–8 weeks', 'color': '#ff9c40',
                'skills': ['Supervised Learning', 'Unsupervised Learning', 'Scikit-learn', 'Model Evaluation'],
                'courses': [
                    {'name': 'Machine Learning by Andrew Ng', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/machine-learning-introduction', 'price': 'Free Audit', 'rating': 4.9},
                    {'name': 'ML A-Z 2024', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/machinelearning/', 'price': '₹499', 'rating': 4.5},
                ],
                'practice': [
                    {'name': 'Kaggle Competitions', 'platform': 'Kaggle', 'url': 'https://www.kaggle.com/competitions'},
                ],
            },
            {
                'phase': 4, 'title': 'Build Portfolio Projects',
                'duration': '4 weeks', 'color': '#ff7700',
                'skills': ['End-to-End Projects', 'GitHub', 'Storytelling with Data', 'Deployment'],
                'courses': [
                    {'name': 'Applied Data Science Capstone', 'platform': 'Coursera', 'url': 'https://www.coursera.org/learn/applied-data-science-capstone', 'price': 'Free Audit', 'rating': 4.6},
                ],
                'practice': [
                    {'name': 'Open Datasets', 'platform': 'Kaggle', 'url': 'https://www.kaggle.com/datasets'},
                ],
            },
            {
                'phase': 5, 'title': 'Apply for Jobs',
                'duration': 'Ongoing', 'color': '#e03000',
                'skills': ['Resume Building', 'DSA Interview Prep', 'SQL', 'System Design Basics'],
                'courses': [
                    {'name': 'SQL for Data Analysis', 'platform': 'Udacity', 'url': 'https://www.udacity.com/course/sql-for-data-analysis--ud198', 'price': 'Free', 'rating': 4.5},
                ],
                'practice': [
                    {'name': 'Data Science Jobs', 'platform': 'LinkedIn', 'url': 'https://www.linkedin.com/jobs/data-scientist-jobs/'},
                    {'name': 'Data Science Jobs India', 'platform': 'Naukri', 'url': 'https://www.naukri.com/data-scientist-jobs'},
                ],
            },
        ],
        'scholarships': [
            {'name': 'Google Data Analytics Certificate Aid', 'url': 'https://grow.google/certificates/', 'amount': 'Free Course'},
            {'name': 'Coursera Financial Aid', 'url': 'https://www.coursera.org/financial-aid', 'amount': 'Full Scholarship'},
        ],
        'avg_salary': '₹8–20 LPA',
        'top_companies': ['Google', 'Amazon', 'Flipkart', 'Swiggy', 'Zepto', 'TCS', 'Infosys'],
    },
    'web developer': {
        'title': 'Full Stack Web Developer',
        'emoji': '🌐',
        'duration': '6–9 months',
        'phases': [
            {
                'phase': 1, 'title': 'HTML, CSS & Design Basics',
                'duration': '3–4 weeks', 'color': '#ff6a00',
                'skills': ['HTML5', 'CSS3', 'Flexbox', 'Responsive Design', 'Bootstrap'],
                'courses': [
                    {'name': 'Responsive Web Design', 'platform': 'freeCodeCamp', 'url': 'https://www.freecodecamp.org/learn/2022/responsive-web-design/', 'price': 'Free', 'rating': 4.9},
                    {'name': 'HTML & CSS Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/html-and-css-bootcamp/', 'price': '₹499', 'rating': 4.7},
                ],
                'practice': [
                    {'name': 'Frontend Challenges', 'platform': 'Frontend Mentor', 'url': 'https://www.frontendmentor.io/challenges'},
                ],
            },
            {
                'phase': 2, 'title': 'JavaScript & React',
                'duration': '6–8 weeks', 'color': '#cc2200',
                'skills': ['JavaScript ES6+', 'DOM Manipulation', 'React', 'State Management', 'API Integration'],
                'courses': [
                    {'name': 'JavaScript Algorithms & DS', 'platform': 'freeCodeCamp', 'url': 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/', 'price': 'Free', 'rating': 4.8},
                    {'name': 'React - The Complete Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/react-the-complete-guide-incl-redux/', 'price': '₹499', 'rating': 4.7},
                ],
                'practice': [
                    {'name': 'JS Challenges', 'platform': 'HackerRank', 'url': 'https://www.hackerrank.com/domains/tutorials/10-days-of-javascript'},
                    {'name': 'JS Practice', 'platform': 'LeetCode', 'url': 'https://leetcode.com/problemset/?topicSlugs=javascript'},
                ],
            },
            {
                'phase': 3, 'title': 'Backend: Node.js / Python',
                'duration': '4–6 weeks', 'color': '#ff9c40',
                'skills': ['Node.js', 'Express', 'REST APIs', 'Databases', 'Authentication'],
                'courses': [
                    {'name': 'NodeJS - The Complete Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/nodejs-the-complete-guide/', 'price': '₹499', 'rating': 4.7},
                    {'name': 'Full Stack Open', 'platform': 'University of Helsinki', 'url': 'https://fullstackopen.com/en/', 'price': 'Free', 'rating': 4.9},
                ],
                'practice': [
                    {'name': 'Backend Projects', 'platform': 'GitHub', 'url': 'https://github.com/topics/nodejs-projects'},
                ],
            },
            {
                'phase': 4, 'title': 'Apply for Jobs',
                'duration': 'Ongoing', 'color': '#e03000',
                'skills': ['Portfolio Site', 'GitHub Profile', 'DSA for Interviews', 'System Design'],
                'courses': [],
                'practice': [
                    {'name': 'Web Dev Jobs', 'platform': 'LinkedIn', 'url': 'https://www.linkedin.com/jobs/web-developer-jobs/'},
                    {'name': 'Web Dev Jobs India', 'platform': 'Naukri', 'url': 'https://www.naukri.com/web-developer-jobs'},
                ],
            },
        ],
        'scholarships': [
            {'name': 'Meta Frontend Developer Cert Aid', 'url': 'https://www.coursera.org/professional-certificates/meta-front-end-developer', 'amount': 'Financial Aid'},
            {'name': 'Google UX Design Scholarship', 'url': 'https://grow.google/certificates/', 'amount': 'Free Course'},
        ],
        'avg_salary': '₹5–15 LPA',
        'top_companies': ['Infosys', 'Wipro', 'TCS', 'Razorpay', 'Zepto', 'Freshworks', 'CRED'],
    },
    'python developer': {
        'title': 'Python Developer',
        'emoji': '🐍',
        'duration': '5–8 months',
        'phases': [
            {
                'phase': 1, 'title': 'Python Fundamentals',
                'duration': '4–5 weeks', 'color': '#ff6a00',
                'skills': ['Variables', 'Data Types', 'Functions', 'OOP', 'File Handling'],
                'courses': [
                    {'name': 'Python Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/complete-python-bootcamp/', 'price': '₹499', 'rating': 4.7},
                    {'name': 'Python for Everybody', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/python', 'price': 'Free Audit', 'rating': 4.8},
                ],
                'practice': [
                    {'name': 'Python Challenges', 'platform': 'HackerRank', 'url': 'https://www.hackerrank.com/domains/python'},
                ],
            },
            {
                'phase': 2, 'title': 'Advanced Python & Libraries',
                'duration': '4–6 weeks', 'color': '#cc2200',
                'skills': ['NumPy', 'Pandas', 'Requests', 'Flask/Django', 'Web Scraping'],
                'courses': [
                    {'name': 'Python Django 2024', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp/', 'price': '₹499', 'rating': 4.5},
                    {'name': 'Automate the Boring Stuff', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/automate/', 'price': 'Free', 'rating': 4.7},
                ],
                'practice': [
                    {'name': 'Python Practice', 'platform': 'LeetCode', 'url': 'https://leetcode.com/problemset/'},
                    {'name': 'Python Projects', 'platform': 'GeeksForGeeks', 'url': 'https://www.geeksforgeeks.org/python-projects-beginner-to-advanced/'},
                ],
            },
            {
                'phase': 3, 'title': 'Projects & Portfolio',
                'duration': '4 weeks', 'color': '#ff9c40',
                'skills': ['GitHub', 'APIs', 'Deployment', 'Docker Basics'],
                'courses': [
                    {'name': 'Git & GitHub Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/git-and-github-bootcamp/', 'price': '₹499', 'rating': 4.7},
                ],
                'practice': [
                    {'name': 'Open Source Projects', 'platform': 'GitHub', 'url': 'https://github.com/topics/python'},
                ],
            },
            {
                'phase': 4, 'title': 'Apply for Jobs',
                'duration': 'Ongoing', 'color': '#e03000',
                'skills': ['DSA', 'System Design', 'Interview Prep'],
                'courses': [],
                'practice': [
                    {'name': 'Python Jobs', 'platform': 'LinkedIn', 'url': 'https://www.linkedin.com/jobs/python-developer-jobs/'},
                    {'name': 'Python Jobs India', 'platform': 'Naukri', 'url': 'https://www.naukri.com/python-developer-jobs'},
                ],
            },
        ],
        'scholarships': [
            {'name': 'Coursera Financial Aid', 'url': 'https://www.coursera.org/financial-aid', 'amount': 'Full Scholarship'},
        ],
        'avg_salary': '₹4–12 LPA',
        'top_companies': ['TCS', 'Infosys', 'Wipro', 'Amazon', 'Freshworks', 'Razorpay'],
    },
}

def get_default_roadmap(goal, level):
    """Generate a dynamic roadmap for any career goal not in templates."""
    goal_lower = goal.lower()
    encoded = urllib.parse.quote(goal)
    phases = [
        {
            'phase': 1, 'title': f'Learn {goal.title()} Fundamentals',
            'duration': '4–6 weeks', 'color': '#ff6a00',
            'skills': [f'{goal.title()} Basics', 'Core Concepts', 'Tools & Setup', 'Best Practices'],
            'courses': [
                {'name': f'{goal.title()} Beginner Course', 'platform': 'Udemy', 'url': f'https://www.udemy.com/courses/search/?q={encoded}', 'price': '₹499–₹999', 'rating': 4.5},
                {'name': f'{goal.title()} on Coursera', 'platform': 'Coursera', 'url': f'https://www.coursera.org/search?query={encoded}', 'price': 'Free Audit', 'rating': 4.6},
                {'name': f'{goal.title()} Tutorial', 'platform': 'YouTube', 'url': f'https://www.youtube.com/results?search_query={encoded}+tutorial', 'price': 'Free', 'rating': 4.4},
            ],
            'practice': [],
        },
        {
            'phase': 2, 'title': 'Intermediate Skills & Projects',
            'duration': '6–8 weeks', 'color': '#cc2200',
            'skills': ['Intermediate Concepts', 'Real Projects', 'Problem Solving', 'Industry Tools'],
            'courses': [
                {'name': f'Advanced {goal.title()}', 'platform': 'edX', 'url': f'https://www.edx.org/search?q={encoded}', 'price': 'Free', 'rating': 4.5},
                {'name': f'{goal.title()} Masterclass', 'platform': 'Skillshare', 'url': f'https://www.skillshare.com/search?query={encoded}', 'price': 'Subscription', 'rating': 4.3},
            ],
            'practice': [
                {'name': f'{goal.title()} Practice', 'platform': 'HackerRank', 'url': f'https://www.hackerrank.com/domains/tutorials/10-days-of-javascript'},
            ],
        },
        {
            'phase': 3, 'title': 'Build Portfolio & Apply',
            'duration': '4–6 weeks', 'color': '#ff9c40',
            'skills': ['Portfolio Projects', 'Resume Building', 'Interview Prep', 'Networking'],
            'courses': [],
            'practice': [
                {'name': f'{goal.title()} Jobs', 'platform': 'LinkedIn', 'url': f'https://www.linkedin.com/jobs/search/?keywords={encoded}'},
                {'name': f'{goal.title()} Jobs India', 'platform': 'Naukri', 'url': f'https://www.naukri.com/{goal_lower.replace(" ", "-")}-jobs'},
                {'name': f'{goal.title()} Scholarships', 'platform': 'Buddy4Study', 'url': f'https://www.buddy4study.com/scholarships?q={encoded}'},
            ],
        },
    ]
    return {
        'title': goal.title(),
        'emoji': '🎯',
        'duration': '6–10 months',
        'phases': phases,
        'scholarships': [
            {'name': 'Coursera Financial Aid', 'url': 'https://www.coursera.org/financial-aid', 'amount': 'Full Scholarship'},
            {'name': 'NSP Scholarship', 'url': 'https://scholarships.gov.in', 'amount': 'Up to ₹1 Lakh'},
        ],
        'avg_salary': 'Varies by role',
        'top_companies': ['TCS', 'Infosys', 'Wipro', 'Amazon', 'Google', 'Flipkart'],
    }

def generate_roadmap(goal, level='beginner'):
    """Main function: returns roadmap data for a given career goal."""
    goal_lower = goal.lower().strip()
    # Check known templates
    for key, data in ROADMAP_TEMPLATES.items():
        if key in goal_lower or goal_lower in key:
            return data
    # Dynamic fallback
    return get_default_roadmap(goal, level)
