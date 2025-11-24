"""
-----------------------------------------------------------------------
PROJECT: SolSearch - Professional Job Application Tracker
AUTHOR: Tim
COURSE: DSA 214

DESCRIPTION:
This is a program to help students track their job applications.
It acts like a digital notebook where you can add jobs, update their status,
and see statistics about how you are doing.

HOW TO READ THIS CODE:
1. "Imports" are tools we borrow from Python.
2. "Classes" are like buckets that hold specific jobs (one bucket for the Database, 
   one for Math, one for the Screen).
3. "Functions" (def) are the actual actions the code performs.
-----------------------------------------------------------------------
"""

# --- IMPORTS ---
# We need to borrow some tools to build this house.
import sqlite3          # The tool for managing the database file.
import sys              # Tools for interacting with the computer system.
import os               # Tools for clearing the screen (cleaning up).
import csv              # A tool to save data into Excel-compatible files.
import statistics       # A math tool to calculate averages easily.
import matplotlib.pyplot as plt # A tool to draw charts and graphs.
from datetime import datetime   # A tool to check if dates are real.

# --- SETTINGS ---
# We put these names here at the top. If we want to change the database name later,
# we only have to change it in this one spot.
DB_NAME = "solsearch.db"
VALID_STATUSES = ["Applied", "Interview", "Rejected", "Offer"]

class DatabaseManager:
    """
    RESPONSIBILITY: The Librarian.
    This class handles everything related to the database file. 
    It is the only part of the code allowed to touch the hard drive.
    """
    def __init__(self, db_name):
        """
        This runs automatically when the program starts.
        It saves the database name and makes sure the table exists.
        """
        self.db_name = db_name
        self.initialize_db()

    def get_connection(self):
        """
        Opens the door to the database file so we can read/write to it.
        """
        return sqlite3.connect(self.db_name)

    def initialize_db(self):
        """
        Sets up the empty filing cabinet (Table) if it doesn't exist yet.
        It defines the columns:
        - ID: A unique number for every job (1, 2, 3...).
        - Company: Who we applied to.
        - Role: What the job title is.
        - Priority: How much we want the job (1-5).
        """
        conn = self.get_connection()
        cursor = conn.cursor() # The 'cursor' is like a pen that writes SQL commands.
        
        # We use SQL (Structured Query Language) to create the table.
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
        conn.commit() # Save the changes.
        conn.close()  # Close the door.

    def execute_write(self, query, params=()):
        """
        Used for Adding, Updating, or Deleting data.
        
        SECURITY NOTE (Very Important):
        We pass data in a separate tuple called 'params' instead of pasting it
        directly into the text. This prevents 'SQL Injection', a common way
        hackers break into databases.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit() # Save the change permanently.
            return True
        except sqlite3.Error as e:
            # If something breaks (like the file is locked), print the error.
            print(f"❌ Database Error: {e}")
            return False
        finally:
            # This runs no matter what, ensuring the database connection always closes.
            conn.close()

    def fetch_all(self, query, params=()):
        """
        Used for Reading data. It asks the database a question and returns the answer.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall() # Get all the results.
        conn.close()
        return rows

class AnalyticsEngine:
    """
    RESPONSIBILITY: The Analyst.
    This class handles the math, the statistics, the charts, and exporting files.
    It asks the DatabaseManager for data, then does smart things with it.
    """
    def __init__(self, db_manager):
        self.db = db_manager

    def generate_funnel_report(self):
        """
        Calculates percentages.
        Example: If you have 10 apps and 2 rejections, that's a 20% rejection rate.
        """
        # SQL COUNT(*) counts how many rows exist for each status.
        rows = self.db.fetch_all("SELECT status, COUNT(*) FROM applications GROUP BY status")
        
        # Calculate total applications using Python's sum() function.
        total_apps = sum(row[1] for row in rows)
        
        print("\n📊 --- FUNNEL ANALYSIS ---")
        if total_apps == 0:
            print("No data available yet.")
            return

        for status, count in rows:
            percentage = (count / total_apps) * 100
            # We format the percentage to show only 1 decimal place (e.g., 33.3%).
            print(f" > {status:<15}: {count} ({percentage:.1f}%)")

    def priority_stats(self):
        """
        Calculates the Average (Mean) and the Middle Point (Median) of your priorities.
        This tells you if you are applying for jobs you really want, or just random ones.
        """
        rows = self.db.fetch_all("SELECT priority FROM applications")
        if not rows: return

        # Convert the database rows into a simple list of numbers [1, 5, 3, 2...]
        priorities = [r[0] for r in rows]
        
        mean_val = statistics.mean(priorities)
        median_val = statistics.median(priorities)
        
        print("\n🎯 --- PRIORITY ALIGNMENT ---")
        print(f" > Total Apps:      {len(priorities)}")
        print(f" > Average Score:   {mean_val:.2f} / 5.0")
        print(f" > Median Score:    {median_val:.2f} / 5.0")

    def generate_chart(self):
        """
        Creates a Bar Chart image.
        We save it as a file (.png) instead of popping up a window, 
        because pop-up windows can sometimes freeze command-line apps.
        """
        rows = self.db.fetch_all("SELECT status, COUNT(*) FROM applications GROUP BY status")
        if not rows:
            print("Not enough data for chart.")
            return

        # Separate the data into Names (X-axis) and Numbers (Y-axis)
        statuses = [row[0] for row in rows]
        counts = [row[1] for row in rows]

        try:
            plt.figure(figsize=(8, 5)) # Set image size
            colors = ['#3498db', '#f1c40f', '#e74c3c', '#2ecc71'] # Blue, Yellow, Red, Green
            plt.bar(statuses, counts, color=colors[:len(statuses)])
            plt.title("SolSearch: Application Status Distribution")
            plt.xlabel("Status")
            plt.ylabel("Count")
            plt.grid(axis='y', linestyle='--', alpha=0.7) # Add faint grid lines
            
            filename = "solsearch_analytics.png"
            plt.savefig(filename) # Save the picture to the folder
            plt.close() # Clear the memory
            print(f"\n✅ Chart saved as '{filename}'")
        except Exception as e:
            print(f"Error generating chart: {e}")

    def export_to_csv(self):
        """
        Exports the database to a CSV file (Excel).
        This is useful if you want to move your data to another computer.
        """
        rows = self.db.fetch_all("SELECT * FROM applications")
        filename = "solsearch_export.csv"
        
        try:
            # 'w' means Write mode. 'newline=""' prevents blank lines between rows.
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write the Title Row first
                writer.writerow(["ID", "Company", "Role", "Date Applied", "Status", "Priority"])
                # Write all the database rows
                writer.writerows(rows)
            print(f"\n✅ Data exported successfully to '{filename}'")
        except Exception as e:
            print(f"❌ Error exporting data: {e}")

class UserInterface:
    """
    RESPONSIBILITY: The Decorator & Bouncer.
    This class handles 2 things:
    1. Making things look pretty (Banners, Stars, Tables).
    2. Checking user input (The Bouncer) to make sure no bad data gets in.
    """
    
    @staticmethod
    def clear_screen():
        """Wipes the terminal text so the app looks like a clean screen."""
        # Checks if you are on Windows ('nt') or Mac/Linux and runs the right command.
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_banner():
        """Prints the ASCII Art Logo at the top of the menu."""
        print(r"""
   _____       __ _____                     __     
  / ___/____  / // ___/___  ____ __________/ /_    
  \__ \/ __ \/ /\__ \/ _ \/ __ `/ ___/ ___/ __ \   
 ___/ / /_/ / /___/ /  __/ /_/ / /  / /__/ / / /   
/____/\____/_//____/\___/\__,_/_/   \___/_/ /_/    
        :: Career Tracking System v2.0 ::          
        """)

    @staticmethod
    def format_cell(text, width):
        """
        This ensures the table stays aligned.
        If a role name is too long (e.g. 'Senior Engineering Manager'), 
        it cuts it off and adds dots: 'Senior Enginee...'
        """
        text = str(text)
        if len(text) > width:
            return text[:width-3] + "..."
        return text

    @staticmethod
    def stars(priority):
        """
        Visual Trick: Converts the number 5 into '⭐⭐⭐⭐⭐'.
        It makes the table look much nicer to read.
        """
        return "⭐" * priority

    def pause(self):
        """Stops the program so the user has time to read the results."""
        input("\nPress [Enter] to return to menu...")

    # --- INPUT VALIDATION (THE BOUNCER) ---
    # These functions use 'while True' loops. They lock the user in a loop
    # until they type the correct information. This prevents crashes.

    @staticmethod
    def get_valid_string(prompt):
        """Ensures the user doesn't just press Enter without typing."""
        while True:
            s = input(prompt).strip()
            if s: return s
            print("⚠️ Input cannot be empty.")

    @staticmethod
    def get_valid_priority():
        """Ensures the user types a Number, not text."""
        while True:
            try:
                val = int(input("Priority (1-5): "))
                if 1 <= val <= 5: return val
                print("⚠️ Enter a number 1-5.")
            except ValueError:
                # This creates a 'Safety Net'. If they type "Hello", it catches the error.
                print("⚠️ Invalid input.")

    @staticmethod
    def get_valid_date():
        """Ensures the user types a real date in the right format."""
        while True:
            d = input("Date Applied (YYYY-MM-DD): ").strip()
            try:
                # This checks if the date actually exists (e.g. Feb 30th will fail).
                datetime.strptime(d, "%Y-%m-%d")
                return d
            except ValueError:
                print("⚠️ Invalid format. Use YYYY-MM-DD.")

    @staticmethod
    def get_valid_status():
        """Ensures the user types one of the approved status words."""
        print(f"Options: {' / '.join(VALID_STATUSES)}")
        while True:
            s = input("Status: ").strip().title()
            if s in VALID_STATUSES: return s
            print("⚠️ Invalid Status.")

def main():
    """
    RESPONSIBILITY: The Boss.
    This function coordinates the Database, the Math, and the UI.
    It runs in an infinite loop until the user chooses to Exit.
    """
    db = DatabaseManager(DB_NAME)
    analytics = AnalyticsEngine(db)
    ui = UserInterface()

    while True:
        # Step 1: Clean the screen and show the logo
        ui.clear_screen()
        ui.print_banner()
        
        # Step 2: Show the Menu Options
        print("1. ➕ Add New Application")
        print("2. 📋 View History (Sortable)")
        print("3. ✏️  Update Status")
        print("4. 🗑️  Delete Entry")
        print("5. 📊 Analytics Dashboard")
        print("6. 💾 Export to CSV")
        print("7. 🚪 Exit")
        print("-" * 40)

        choice = input("Select Option: ")

        # Step 3: Handle the User's Choice
        if choice == '1':
            # --- CREATE (Adding Data) ---
            print("\n--- ADD NEW APPLICATION ---")
            # Gather data using our safe input methods
            company = ui.get_valid_string("Company Name: ")
            role = ui.get_valid_string("Role Title: ")
            date = ui.get_valid_date()
            status = ui.get_valid_status()
            priority = ui.get_valid_priority()
            
            # The '?' marks are placeholders for the data.
            sql = "INSERT INTO applications (company, role, date_applied, status, priority) VALUES (?, ?, ?, ?, ?)"
            if db.execute_write(sql, (company, role, date, status, priority)):
                print("✅ Application logged successfully.")
            ui.pause()

        elif choice == '2':
            # --- READ (Viewing Data) ---
            ui.clear_screen()
            ui.print_banner()
            print("\n--- APPLICATION HISTORY ---")
            
            print("Sort by: [1] ID (Default)  [2] Company  [3] Status  [4] Priority (High->Low)")
            sort_choice = input("Choice: ").strip()
            
            # Map the user's choice (1, 2, 3) to actual SQL commands.
            sort_map = {
                '1': "id ASC",       # Sort by ID (1, 2, 3...)
                '2': "company ASC",  # Sort A-Z
                '3': "status ASC",   # Sort A-Z
                '4': "priority DESC" # Sort 5 stars to 1 star
            }
            
            # If they typed garbage, default to ID sorting.
            order_clause = sort_map.get(sort_choice, "id ASC")
            
            rows = db.fetch_all(f"SELECT * FROM applications ORDER BY {order_clause}")
            
            # Print the Table Headers
            print(f"{'ID':<4} {'Company':<18} {'Role':<18} {'Date':<12} {'Status':<10} {'Priority':<10}")
            print("=" * 78)
            
            if not rows:
                print("No records found.")
            else:
                for r in rows:
                    # Clean up the text so it fits in the table
                    c_comp = ui.format_cell(r[1], 18)
                    c_role = ui.format_cell(r[2], 18)
                    c_stars = ui.stars(r[5]) 
                    # Print the row
                    print(f"{r[0]:<4} {c_comp:<18} {c_role:<18} {r[3]:<12} {r[4]:<10} {c_stars:<10}")
            ui.pause()

        elif choice == '3':
            # --- UPDATE (Changing Data) ---
            print("\n--- UPDATE STATUS ---")
            # Show a mini-list so the user knows which ID to pick
            rows = db.fetch_all("SELECT id, company, role, status FROM applications")
            if not rows:
                print("No applications.")
            else:
                for r in rows:
                    print(f"ID: {r[0]} | {r[1]} ({r[3]})")
                print("-" * 30)
                try:
                    app_id = int(input("Enter ID to update: "))
                    new_status = ui.get_valid_status()
                    sql = "UPDATE applications SET status = ? WHERE id = ?"
                    if db.execute_write(sql, (new_status, app_id)):
                        print("✅ Status updated.")
                except ValueError:
                    print("⚠️ ID must be a number.")
            ui.pause()

        elif choice == '4':
            # --- DELETE (Removing Data) ---
            print("\n--- DELETE ENTRY ---")
            rows = db.fetch_all("SELECT id, company, role FROM applications")
            for r in rows:
                print(f"ID: {r[0]} | {r[1]} - {r[2]}")
            try:
                app_id = int(input("\nEnter ID to DELETE: "))
                # Ask for confirmation so they don't delete by accident
                confirm = input(f"Delete ID {app_id}? (yes/no): ").lower()
                if confirm == 'yes':
                    sql = "DELETE FROM applications WHERE id = ?"
                    if db.execute_write(sql, (app_id,)):
                        print("🗑️ Application deleted.")
                else:
                    print("Cancelled.")
            except ValueError:
                print("⚠️ ID must be a number.")
            ui.pause()

        elif choice == '5':
            # --- ANALYTICS ---
            ui.clear_screen()
            ui.print_banner()
            analytics.generate_funnel_report()
            analytics.priority_stats()
            analytics.generate_chart()
            ui.pause()
            
        elif choice == '6':
            # --- EXPORT ---
            analytics.export_to_csv()
            ui.pause()

        elif choice == '7':
            print("\nGood luck with the job hunt! 🚀")
            break
        else:
            print("⚠️ Invalid option.")
            ui.pause()

# This line makes sure the program only runs if we run this file directly.
if __name__ == "__main__":
    main()