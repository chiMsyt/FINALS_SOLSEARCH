"""
SCRIPT: seed_data.py
PURPOSE: Generates dummy data for testing the main application.
"""

import sqlite3
import random
import os
from datetime import datetime, timedelta

DB_NAME = "solsearch.db"
NUM_ENTRIES = 1000  

# Expanded Data Pools
COMPANIES = [
    # Big Tech
    "Google", "Amazon", "Microsoft", "Apple", "Meta", "Netflix", "Tesla", "NVIDIA",
    # Fintech / Finance
    "Stripe", "PayPal", "Square", "Goldman Sachs", "JP Morgan", "Morgan Stanley", 
    "BlackRock", "Citadel", "Jane Street", "Coinbase", "Robinhood",
    # Enterprise / Cloud
    "Salesforce", "Oracle", "SAP", "Snowflake", "Datadog", "Atlassian", "ServiceNow",
    "IBM", "Intel", "AMD", "Cisco",
    # Startups / Unicorns
    "OpenAI", "Anthropic", "SpaceX", "Discord", "Notion", "Figma", "Canva", 
    "Airbnb", "Uber", "Lyft", "DoorDash", "Instacart", "Plaid",
    # Traditional / Retail / Other
    "Walmart", "Target", "Costco", "Nike", "Adidas", "Ford", "GM", "Boeing",
    "Lockheed Martin", "McKinsey", "BCG", "Bain", "Deloitte", "PwC",
    "The New York Times", "Disney", "Hulu", "Spotify", "Epic Games"
]

ROLES = [
    # Software Engineering
    "Software Engineer I", "Software Engineer II", "Senior Software Engineer",
    "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "DevOps Engineer", "Site Reliability Engineer (SRE)", "Mobile Developer (iOS)",
    "Mobile Developer (Android)", "Embedded Systems Engineer",
    # Data & AI
    "Data Scientist", "Data Analyst", "Machine Learning Engineer",
    "AI Research Scientist", "Data Engineer", "Business Intelligence Analyst",
    # Product & Design
    "Product Manager", "Associate Product Manager", "Technical Product Manager",
    "UI/UX Designer", "Product Designer", "User Researcher",
    # IT & Cyber
    "IT Support Specialist", "System Administrator", "Cybersecurity Analyst",
    "Network Engineer", "Cloud Architect",
    # Business / Other
    "Technical Program Manager", "Solutions Architect", "Sales Engineer",
    "Developer Advocate", "QA Engineer", "Technical Writer"
]

STATUSES = ["Applied", "Interview", "Rejected", "Offer"]
# Weighted: Mostly applied/rejected, fewer interviews, rare offers
STATUS_WEIGHTS = [0.45, 0.15, 0.35, 0.05] 

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_random_date():
    """Returns a random date string from the last 120 days."""
    days_ago = random.randint(0, 120)
    date_obj = datetime.now() - timedelta(days=days_ago)
    return date_obj.strftime("%Y-%m-%d")

def connect_db():
    return sqlite3.connect(DB_NAME)

def wipe_database():
    """Deletes all records and resets ID counter."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='applications';")
        if cursor.fetchone():
            cursor.execute("DELETE FROM applications")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='applications'") 
            conn.commit()
            print("Database cleared.")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def generate_data():
    conn = connect_db()
    cursor = conn.cursor()

    # Create table if script is run before main.py
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            date_applied TEXT NOT NULL,
            status TEXT NOT NULL,
            priority INTEGER NOT NULL
        )
    ''')

    print(f"Generating {NUM_ENTRIES} entries from {len(COMPANIES)} companies and {len(ROLES)} roles...")

    for _ in range(NUM_ENTRIES):
        company = random.choice(COMPANIES)
        role = random.choice(ROLES)
        date_applied = get_random_date()
        
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
        
        # Skew priority: Higher priority for big tech or offers (simulation logic)
        if status == "Offer" or company in ["Google", "OpenAI", "Netflix"]:
            priority = random.randint(4, 5)
        else:
            priority = random.randint(1, 5)

        cursor.execute(
            "INSERT INTO applications (company, role, date_applied, status, priority) VALUES (?, ?, ?, ?, ?)",
            (company, role, date_applied, status, priority)
        )

    conn.commit()
    conn.close()
    print("Done.")

if __name__ == "__main__":
    clear_screen()
    print("--- DATA SEEDER v2.0 ---")
    choice = input("Wipe existing data? (y/n): ").lower()
    
    if choice == 'y':
        wipe_database()
    
    generate_data()
    print(f"\nSeed complete. Run 'python gui_app.py' to view {NUM_ENTRIES} records.")