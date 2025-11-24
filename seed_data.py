"""
-----------------------------------------------------------------------
SCRIPT: seed_data.py
PURPOSE: Generates dummy data for the SolSearch application.
USE CASE: Run this once before your demo to populate the DB with
          realistic data for charts and analysis.
-----------------------------------------------------------------------
"""

import sqlite3
import random
import os # Added for screen clearing
from datetime import datetime, timedelta

# CONFIGURATION
DB_NAME = "solsearch.db"
# ## STUDENT NOTE: Change this number to generate more/less data.
# 50 is a good number to make the analytics look robust.
NUM_ENTRIES = 100  

# DATA POOLS (To make the data look real)
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
# Weighted probabilities: Realistically, you get more Rejections/Applied than Offers.
STATUS_WEIGHTS = [0.4, 0.2, 0.35, 0.05] 

def clear_screen():
    """Clears the terminal window."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_random_date():
    """Generates a random date within the last 3 months."""
    days_ago = random.randint(0, 90)
    date_obj = datetime.now() - timedelta(days=days_ago)
    return date_obj.strftime("%Y-%m-%d")

def connect_db():
    return sqlite3.connect(DB_NAME)

def wipe_database():
    """Optional: Clears existing data so you don't have duplicates."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Check if table exists first to avoid errors
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='applications';")
        if cursor.fetchone():
            cursor.execute("DELETE FROM applications")
            # Reset the Auto-Increment counter to 0
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='applications'") 
            conn.commit()
            print("🧹 Database wiped clean.")
        else:
            print("⚠️ Table not found. It will be created automatically.")
    except sqlite3.Error as e:
        print(f"Error wiping DB: {e}")
    finally:
        conn.close()

def generate_data():
    """Inserts random rows into the database."""
    conn = connect_db()
    cursor = conn.cursor()

    # Ensure table exists (in case you run this before main.py)
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

    print(f"🌱 Seeding {NUM_ENTRIES} entries...")

    for _ in range(NUM_ENTRIES):
        company = random.choice(COMPANIES)
        role = random.choice(ROLES)
        date_applied = get_random_date()
        
        # Pick a status based on probability weights
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
        
        # Random priority 1-5
        priority = random.randint(1, 5)

        # Parameterized Query (Good Practice even in scripts!)
        cursor.execute(
            "INSERT INTO applications (company, role, date_applied, status, priority) VALUES (?, ?, ?, ?, ?)",
            (company, role, date_applied, status, priority)
        )

    conn.commit()
    conn.close()
    print("✅ Success! Database populated.")

if __name__ == "__main__":
    clear_screen()
    print(r"""
   _____       __ _____                     __     
  / ___/____  / // ___/___  ____ __________/ /_    
  \__ \/ __ \/ /\__ \/ _ \/ __ `/ ___/ ___/ __ \   
 ___/ / /_/ / /___/ /  __/ /_/ / /  / /__/ / / /   
/____/\____/_//____/\___/\__,_/_/   \___/_/ /_/    
        :: DATA GENERATOR TOOL ::          
        """)
    print("--- SOLSEARCH DATA SEEDER ---")
    choice = input("Do you want to WIPE existing data before generating? (y/n): ").lower()
    
    if choice == 'y':
        wipe_database()
    
    generate_data()
    print("\n👉 Now run 'python main.py' to see your data!")