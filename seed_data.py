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

# Expanded Data Pools - Focused on Tech/IT Ecosystems
COMPANIES = [
    # --- MAANG / Big Tech ---
    "Google", "Amazon", "Microsoft", "Apple", "Meta", "Netflix", "Tesla", "NVIDIA",
    
    # --- Enterprise Software / SaaS ---
    "Salesforce", "Oracle", "SAP", "ServiceNow", "Workday", "Adobe", "Intuit", 
    "Atlassian", "Autodesk", "VMware", "Red Hat", "Twilio", "Zoom", "Slack",
    "DocuSign", "Dropbox", "Box", "HubSpot", "Zendesk", "Asana", "Monday.com",
    
    # --- Cloud & Infrastructure ---
    "Snowflake", "Datadog", "HashiCorp", "GitLab", "GitHub", "Cloudflare", 
    "Akamai", "Fastly", "DigitalOcean", "Heroku", "MongoDB", "Elastic", "Confluent",
    "Splunk", "New Relic", "Dynatrace",
    
    # --- Cybersecurity ---
    "Palo Alto Networks", "CrowdStrike", "Fortinet", "Zscaler", "Okta", "SentinelOne",
    "Rapid7", "Tenable", "CyberArk", "Proofpoint", "Darktrace", "Check Point",
    
    # --- Fintech / Crypto / Payments ---
    "Stripe", "PayPal", "Square", "Block", "Coinbase", "Robinhood", "Plaid", "Affirm",
    "SoFi", "Chime", "Brex", "Klarna", "Wise", "Revolut", "Nubank", "Monzo",
    "Visa", "Mastercard", "American Express", "Fidelity", "Capital One",
    
    # --- Hardware / Semiconductors ---
    "Intel", "AMD", "Qualcomm", "Broadcom", "TSMC", "Micron", "Texas Instruments",
    "Samsung", "Dell", "HP", "Lenovo", "IBM", "Cisco", "Juniper Networks", "Arista",
    
    # --- Gaming / Interactive ---
    "Epic Games", "Unity", "Roblox", "Electronic Arts", "Activision Blizzard", 
    "Ubisoft", "Take-Two Interactive", "Sony PlayStation", "Nintendo", "Riot Games",
    "Twitch", "Discord",
    
    # --- AI / Data / Startups ---
    "OpenAI", "Anthropic", "Databricks", "Scale AI", "Hugging Face", "Midjourney",
    "Jasper", "Stability AI", "Palantir", "C3.ai",
    
    # --- E-commerce / Gig Economy / Travel ---
    "Uber", "Lyft", "Airbnb", "DoorDash", "Instacart", "Booking.com", "Expedia",
    "Shopify", "Etsy", "Wayfair", "Chewy", "Zillow", "Redfin",
    
    # --- Streaming / Media Tech ---
    "Spotify", "Hulu", "Disney+", "HBO Max", "Roku", "Sonos", "Vimeo",
    
    # --- Tech Consulting (IT Services) ---
    "Accenture", "Capgemini", "Infosys", "Tata Consultancy Services", "Cognizant",
    "Wipro", "Thoughtworks", "EPAM Systems"
]

ROLES = [
    # --- Software Engineering (General) ---
    "Software Engineer Intern", "Junior Software Engineer", "Software Engineer I", 
    "Software Engineer II", "Senior Software Engineer", "Staff Software Engineer",
    "Principal Software Engineer", "Distinguished Engineer", "Engineering Manager",
    
    # --- Frontend / Web ---
    "Frontend Developer", "Senior Frontend Engineer", "UI Engineer", 
    "React Developer", "Vue.js Developer", "Angular Developer", 
    "Web Developer", "Creative Technologist",
    
    # --- Backend / API ---
    "Backend Developer", "Senior Backend Engineer", "API Developer", 
    "Java Developer", "Python Developer", "Go Developer", "Node.js Developer",
    "C++ Developer", "Rust Engineer",
    
    # --- Full Stack ---
    "Full Stack Developer", "Senior Full Stack Engineer", "MERN Stack Developer",
    
    # --- Mobile ---
    "iOS Developer", "Android Developer", "Mobile Engineer", 
    "React Native Developer", "Flutter Developer",
    
    # --- Data & AI ---
    "Data Scientist", "Senior Data Scientist", "Data Analyst", 
    "Machine Learning Engineer", "AI Research Scientist", "Computer Vision Engineer",
    "NLP Engineer", "Big Data Engineer", "ETL Developer", "Data Architect",
    
    # --- Infrastructure / Cloud / DevOps ---
    "DevOps Engineer", "Site Reliability Engineer (SRE)", "Cloud Architect", 
    "Cloud Engineer (AWS)", "Cloud Engineer (Azure)", "Platform Engineer", 
    "Kubernetes Administrator", "Infrastructure Engineer", "Systems Engineer",
    
    # --- Cybersecurity ---
    "Cybersecurity Analyst", "Information Security Manager", "Penetration Tester",
    "Security Engineer", "Application Security Engineer", "SOC Analyst", 
    "Identity & Access Management Specialist", "Network Security Engineer",
    
    # --- Database ---
    "Database Administrator (DBA)", "SQL Developer", "Data Warehouse Architect",
    
    # --- Network / IT Support ---
    "Network Engineer", "Network Administrator", "System Administrator", 
    "IT Support Specialist", "Help Desk Technician", "IT Director",
    
    # --- Quality Assurance / Testing ---
    "QA Engineer", "SDET (Software Development Engineer in Test)", 
    "Automation Engineer", "Manual Tester",
    
    # --- Specialized Tech ---
    "Blockchain Developer", "Smart Contract Engineer", "Game Developer", 
    "Unity Developer", "Unreal Engine Developer", "Embedded Systems Engineer", 
    "Firmware Engineer", "IoT Engineer", "AR/VR Developer"
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
    print(f"\nSeed complete. Run 'python main.py' to view {NUM_ENTRIES} records.")