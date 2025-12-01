"""
PROJECT: SolSearch - Job Application Tracker
AUTHOR: Tim
COURSE: DSA 214
DESCRIPTION: CLI tool to track job applications, status updates, and analytics 
using an SQLite database.
"""

import sqlite3
import sys
import os
import csv
import statistics
import matplotlib.pyplot as plt
from datetime import datetime

DB_NAME = "solsearch.db"
VALID_STATUSES = ["Applied", "Interview", "Rejected", "Offer"]

class DatabaseManager:
    """Handles all direct interactions with the SQLite database."""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.initialize_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def initialize_db(self):
        """Creates the applications table if it doesn't exist."""
        conn = self.get_connection()
        cursor = conn.cursor()
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
        conn.commit()
        conn.close()

    def execute_write(self, query, params=()):
        """
        Executes INSERT, UPDATE, or DELETE queries.
        Returns the number of rows affected.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
            return 0
        finally:
            conn.close()

    def fetch_all(self, query, params=()):
        """Executes SELECT queries and returns all rows."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

class AnalyticsEngine:
    """Handles data processing, statistics calculations, and exports."""
    
    def __init__(self, db_manager):
        self.db = db_manager

    def generate_funnel_report(self):
        """Prints a breakdown of applications by status."""
        rows = self.db.fetch_all("SELECT status, COUNT(*) FROM applications GROUP BY status")
        total_apps = sum(row[1] for row in rows)
        
        print("\n📊 --- FUNNEL ANALYSIS ---")
        if total_apps == 0:
            print("No data available.")
            return

        for status, count in rows:
            pct = (count / total_apps) * 100
            print(f" > {status:<15}: {count} ({pct:.1f}%)")

    def priority_stats(self):
        """Calculates mean and median priority scores."""
        rows = self.db.fetch_all("SELECT priority FROM applications")
        if not rows: return

        # Extract priorities into a list
        priorities = [r[0] for r in rows]
        
        print("\n🎯 --- PRIORITY ALIGNMENT ---")
        print(f" > Total Apps:      {len(priorities)}")
        print(f" > Average Score:   {statistics.mean(priorities):.2f} / 5.0")
        print(f" > Median Score:    {statistics.median(priorities):.2f} / 5.0")

    def generate_chart(self):
        """Generates and saves a bar chart of application statuses."""
        rows = self.db.fetch_all("SELECT status, COUNT(*) FROM applications GROUP BY status")
        if not rows:
            print("Not enough data for chart.")
            return

        statuses = [row[0] for row in rows]
        counts = [row[1] for row in rows]

        try:
            plt.figure(figsize=(8, 5))
            # Standard colors
            colors = ['#3498db', '#f1c40f', '#e74c3c', '#2ecc71', '#9b59b6'] 
            plt.bar(statuses, counts, color=colors[:len(statuses)])
            plt.title("Application Status Distribution")
            plt.xlabel("Status")
            plt.ylabel("Count")
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            filename = "solsearch_analytics.png"
            plt.savefig(filename)
            plt.close()
            print(f"\n✅ Chart saved as '{filename}'")
        except Exception as e:
            print(f"Error generating chart: {e}")

    def export_to_csv(self):
        """Dumps database contents to a CSV file."""
        rows = self.db.fetch_all("SELECT * FROM applications")
        filename = "solsearch_export.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Company", "Role", "Date Applied", "Status", "Priority"])
                writer.writerows(rows)
            print(f"\n✅ Data exported to '{filename}'")
        except Exception as e:
            print(f"Error exporting data: {e}")

class UserInterface:
    """Handles formatted output and validates user input."""
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        print(r"""
   _____       __ _____                     __     
  / ___/____  / // ___/___  ____ __________/ /_    
  \__ \/ __ \/ /\__ \/ _ \/ __ `/ ___/ ___/ __ \   
 ___/ / /_/ / /___/ /  __/ /_/ / /  / /__/ / / /   
/____/\____/_//____/\___/\__,_/_/   \___/_/ /_/    
        :: Career Tracking System v1.0 ::          
        """)

    def format_cell(self, text, width):
        """Truncates text to fit table cells."""
        text = str(text)
        if len(text) > width:
            return text[:width-3] + "..."
        return text

    def stars(self, priority):
        """Converts integer priority to star string."""
        return "⭐" * priority

    def pause(self):
        input("\nPress [Enter] to return to menu...")

    def get_valid_string(self, prompt):
        while True:
            s = input(prompt).strip()
            if s: return s
            print("Error: Input cannot be empty.")

    def get_valid_priority(self):
        while True:
            try:
                val = int(input("Priority (1-5): "))
                if 1 <= val <= 5: return val
                print("Error: Enter a number between 1 and 5.")
            except ValueError:
                print("Error: Invalid input.")

    def get_valid_date(self):
        while True:
            d = input("Date Applied (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(d, "%Y-%m-%d")
                return d
            except ValueError:
                print("Error: Invalid format. Use YYYY-MM-DD.")

    def get_valid_status(self):
        print(f"Options: {' / '.join(VALID_STATUSES)}")
        while True:
            s = input("Status: ").strip().title()
            if s in VALID_STATUSES: return s
            print("Error: Invalid Status.")

def main():
    db = DatabaseManager(DB_NAME)
    analytics = AnalyticsEngine(db)
    ui = UserInterface()

    while True:
        ui.clear_screen()
        ui.print_banner()
        
        print("1. Add New Application")
        print("2. View History")
        print("3. Update Status")
        print("4. Delete Entry")
        print("5. Analytics Dashboard")
        print("6. Export to CSV")
        print("7. Exit")
        print("-" * 40)

        choice = input("Select Option: ")

        if choice == '1':
            print("\n--- ADD NEW APPLICATION ---")
            company = ui.get_valid_string("Company Name: ")
            role = ui.get_valid_string("Role Title: ")
            date = ui.get_valid_date()
            status = ui.get_valid_status()
            priority = ui.get_valid_priority()
            
            sql = "INSERT INTO applications (company, role, date_applied, status, priority) VALUES (?, ?, ?, ?, ?)"
            if db.execute_write(sql, (company, role, date, status, priority)) > 0:
                print("✅ Application logged.")
            ui.pause()

        elif choice == '2':
            ui.clear_screen()
            ui.print_banner()
            print("\n--- APPLICATION HISTORY ---")
            print("Sort by: [1] ID  [2] Company  [3] Status  [4] Priority")
            sort_choice = input("Choice: ").strip()
            
            sort_map = {
                '1': "id ASC",
                '2': "company ASC",
                '3': "status ASC",
                '4': "priority DESC"
            }
            order_clause = sort_map.get(sort_choice, "id ASC")
            
            rows = db.fetch_all(f"SELECT * FROM applications ORDER BY {order_clause}")
            
            print(f"{'ID':<4} {'Company':<18} {'Role':<18} {'Date':<12} {'Status':<10} {'Priority':<10}")
            print("=" * 78)
            
            if not rows:
                print("No records found.")
            else:
                for r in rows:
                    c_comp = ui.format_cell(r[1], 18)
                    c_role = ui.format_cell(r[2], 18)
                    c_stars = ui.stars(r[5]) 
                    print(f"{r[0]:<4} {c_comp:<18} {c_role:<18} {r[3]:<12} {r[4]:<10} {c_stars:<10}")
            ui.pause()

        elif choice == '3':
            print("\n--- UPDATE STATUS ---")
            rows = db.fetch_all("SELECT id, company, role, status FROM applications")
            for r in rows:
                print(f"ID: {r[0]} | {r[1]} ({r[3]})")
            print("-" * 30)
            
            try:
                app_id = int(input("Enter ID to update: "))
                new_status = ui.get_valid_status()
                sql = "UPDATE applications SET status = ? WHERE id = ?"
                if db.execute_write(sql, (new_status, app_id)) > 0:
                    print("✅ Status updated.")
                else:
                    print("❌ ID not found.")
            except ValueError:
                print("Error: ID must be a number.")
            ui.pause()

        elif choice == '4':
            print("\n--- DELETE ENTRY ---")
            try:
                app_id = int(input("Enter ID to DELETE: "))
                confirm = input(f"Delete ID {app_id}? (yes/no): ").lower()
                if confirm == 'yes':
                    sql = "DELETE FROM applications WHERE id = ?"
                    if db.execute_write(sql, (app_id,)) > 0:
                        print("🗑️ Application deleted.")
                    else:
                        print("❌ ID not found.")
                else:
                    print("Cancelled.")
            except ValueError:
                print("Error: ID must be a number.")
            ui.pause()

        elif choice == '5':
            ui.clear_screen()
            ui.print_banner()
            analytics.generate_funnel_report()
            analytics.priority_stats()
            analytics.generate_chart()
            ui.pause()
            
        elif choice == '6':
            analytics.export_to_csv()
            ui.pause()

        elif choice == '7':
            print("\nGoodbye!")
            break
        else:
            print("Invalid option.")
            ui.pause()

if __name__ == "__main__":
    main()