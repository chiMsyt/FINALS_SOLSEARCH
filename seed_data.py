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

# Sample data pools
COMPANIES = [
    "Google", "Amazon", "Microsoft", "Spotify", "Netflix", 
    "Tesla", "OpenAI", "Stripe", "Shopify", "StartUp Inc", 
    "Local Bakery", "University Lab", "Goldman Sachs", "JP Morgan"
]

ROLES = [
    "Software Engineer Intern", "Data Analyst", "Product Manager",
    "Frontend Dev", "Backend Dev", "Research Assistant",
    "IT Support", "Cloud Architect", "UX Designer"
]

STATUSES = ["Applied", "Interview", "Rejected", "Offer"]
# Higher probability for rejection/applied than offers
STATUS_WEIGHTS = [0.4, 0.2, 0.35, 0.05] 

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_random_date():
    """Returns a random date string from the last 90 days."""
    days_ago = random.randint(0, 90)
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

    print(f"Generating {NUM_ENTRIES} entries...")

    for _ in range(NUM_ENTRIES):
        company = random.choice(COMPANIES)
        role = random.choice(ROLES)
        date_applied = get_random_date()
        
        # Select status based on defined weights
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
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
    print("--- DATA SEEDER ---")
    choice = input("Wipe existing data? (y/n): ").lower()
    
    if choice == 'y':
        wipe_database()
    
    generate_data()
    print("\nRun 'python main.py' to view data.")