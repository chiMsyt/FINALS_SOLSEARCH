import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import sys

DB_NAME = "solsearch.db"
VALID_STATUSES = ["Applied", "Interview", "Rejected", "Offer"]

"""
TODO: Implement back export .csv, data analysis, and better data visualization features.
"""

LOGO_TEXT = r"""
   _____       __ _____                     __     
  / ___/____  / // ___/___  ____ __________/ /_    
  \__ \/ __ \/ /\__ \/ _ \/ __ `/ ___/ ___/ __ \   
 ___/ / /_/ / /___/ /  __/ /_/ / /  / /__/ / / /   
/____/\____/_//____/\___/\__,_/_/   \___/_/ /_/    
        :: Career Tracking System v2.0 ::          
"""

# ==========================================
# DATABASE MANAGER
# ==========================================
class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.initialize_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def initialize_db(self):
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
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            return 0
        finally:
            conn.close()

    def fetch_all(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

# ==========================================
# GUI APPLICATION
# ==========================================
class SolSearchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager(DB_NAME)
        
        self.title("SolSearch - Job Application Tracker")
        self.geometry("1100x850") 
        
        # Handle the "X" button click to ensure terminal is freed
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        
        style = ttk.Style(self)
        style.theme_use('clam')

        # --- HEADER (ASCII LOGO + EXIT BUTTON) ---
        header_frame = tk.Frame(self, bg="#2c3e50", height=150)
        header_frame.pack(fill="x")
        
        # Grid layout for header
        header_frame.columnconfigure(0, weight=1) # Center spacer
        header_frame.columnconfigure(1, weight=0) # Button column
        
        lbl_logo = tk.Label(
            header_frame, 
            text=LOGO_TEXT, 
            font=("Courier", 10, "bold"), 
            fg="white", 
            bg="#2c3e50",
            justify="left"
        )
        lbl_logo.pack(side="left", padx=20, pady=10)

        # EXIT BUTTON (Standard ASCII Text)
        btn_exit = tk.Button(
            header_frame, 
            text="[X] EXIT APP", 
            font=("Arial", 10, "bold"),
            bg="#c0392b", # Red
            fg="white",
            activebackground="#e74c3c",
            activeforeground="white",
            command=self.close_app,
            width=12,
            height=2
        )
        btn_exit.pack(side="right", padx=20, pady=10)
        
        # --- TABS ---
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: Dashboard
        self.tab_dashboard = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_dashboard, text="Dashboard")
        self.setup_dashboard()

        # Tab 2: List
        self.tab_list = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_list, text="Applications List")
        self.setup_list_view()

        # Tab 3: Add
        self.tab_add = ttk.Frame(self.tabs)
        self.tabs.add(self.tab_add, text="Add New")
        self.setup_add_form()

        # Hook tab change
        self.tabs.bind("<<NotebookTabChanged>>", self.on_tab_change)

    # -----------------------------------------------------------
    # SYSTEM UTILS (Exit Logic)
    # -----------------------------------------------------------
    def close_app(self):
        """Properly closes the GUI and kills the terminal process."""
        if messagebox.askokcancel("Exit", "Close SolSearch?"):
            plt.close('all')  # Close any lingering Matplotlib figures
            self.quit()       # Stop mainloop
            self.destroy()    # Destroy window
            sys.exit()        # Kill Python process to free terminal

    # -----------------------------------------------------------
    # TAB 1: DASHBOARD
    # -----------------------------------------------------------
    def setup_dashboard(self):
        self.stats_frame = ttk.Frame(self.tab_dashboard)
        self.stats_frame.pack(fill="x", pady=10, padx=10)
        
        self.lbl_total = ttk.Label(self.stats_frame, text="Total: 0", font=("Arial", 12, "bold"))
        self.lbl_total.pack(side="left", padx=20)
        
        self.lbl_active = ttk.Label(self.stats_frame, text="Interviews: 0", font=("Arial", 12, "bold"), foreground="blue")
        self.lbl_active.pack(side="left", padx=20)
        
        self.lbl_offers = ttk.Label(self.stats_frame, text="Offers: 0", font=("Arial", 12, "bold"), foreground="green")
        self.lbl_offers.pack(side="left", padx=20)

        self.chart_frame = ttk.Frame(self.tab_dashboard)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.canvas = None

    def refresh_dashboard(self):
        rows = self.db.fetch_all("SELECT status FROM applications")
        total = len(rows)
        interviews = sum(1 for r in rows if r[0] == "Interview")
        offers = sum(1 for r in rows if r[0] == "Offer")

        self.lbl_total.config(text=f"Total Apps: {total}")
        self.lbl_active.config(text=f"Interviews: {interviews}")
        self.lbl_offers.config(text=f"Offers: {offers}")

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        if total == 0:
            lbl = ttk.Label(self.chart_frame, text="No data available.")
            lbl.pack()
            return

        status_counts = {}
        for r in rows:
            status_counts[r[0]] = status_counts.get(r[0], 0) + 1
        
        statuses = list(status_counts.keys())
        counts = list(status_counts.values())

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        colors = ['#3498db', '#f1c40f', '#e74c3c', '#2ecc71']
        bars = ax.bar(statuses, counts, color=colors[:len(statuses)])
        
        ax.set_title("Application Funnel")
        ax.set_ylabel("Count")
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')

        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # -----------------------------------------------------------
    # TAB 2: LIST VIEW (With Sorting)
    # -----------------------------------------------------------
    def setup_list_view(self):
        controls_frame = ttk.Frame(self.tab_list)
        controls_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(controls_frame, text="Refresh", command=self.refresh_list).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Update Status", command=self.update_selected_status).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=5)

        ttk.Label(controls_frame, text="Sort By:").pack(side="left", padx=(20, 5))
        
        self.sort_options = {
            "ID (Newest First)": "id DESC",
            "ID (Oldest First)": "id ASC",
            "Company (A-Z)": "company ASC",
            "Status (A-Z)": "status ASC",
            "Priority (High-Low)": "priority DESC",
            "Priority (Low-High)": "priority ASC"
        }
        
        self.sort_var = tk.StringVar()
        self.combo_sort = ttk.Combobox(controls_frame, textvariable=self.sort_var, values=list(self.sort_options.keys()), state="readonly", width=20)
        self.combo_sort.current(0)
        self.combo_sort.pack(side="left")
        
        self.combo_sort.bind("<<ComboboxSelected>>", lambda e: self.refresh_list())

        columns = ("ID", "Company", "Role", "Date", "Status", "Priority")
        self.tree = ttk.Treeview(self.tab_list, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col == "ID" else 150)

        scrollbar = ttk.Scrollbar(self.tab_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        selected_sort = self.sort_var.get()
        order_clause = self.sort_options.get(selected_sort, "id DESC")
        
        query = f"SELECT * FROM applications ORDER BY {order_clause}"
        rows = self.db.fetch_all(query)
        
        for row in rows:
            display_row = list(row)
            display_row[5] = "*" * int(row[5])
            self.tree.insert("", "end", values=display_row)

    def get_selected_id(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row first.")
            return None
        return self.tree.item(selected_item)['values'][0]

    def delete_selected(self):
        app_id = self.get_selected_id()
        if app_id:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete ID {app_id}?")
            if confirm:
                self.db.execute_write("DELETE FROM applications WHERE id = ?", (app_id,))
                self.refresh_list()
                messagebox.showinfo("Deleted", "Application deleted.")

    def update_selected_status(self):
        app_id = self.get_selected_id()
        if not app_id:
            return

        popup = tk.Toplevel(self)
        popup.title(f"Update ID {app_id}")
        popup.geometry("300x150")

        ttk.Label(popup, text="Select New Status:").pack(pady=10)
        
        status_var = tk.StringVar()
        combo = ttk.Combobox(popup, textvariable=status_var, values=VALID_STATUSES, state="readonly")
        combo.pack(pady=5)
        combo.current(0)

        def save_update():
            new_status = status_var.get()
            self.db.execute_write("UPDATE applications SET status = ? WHERE id = ?", (new_status, app_id))
            self.refresh_list()
            popup.destroy()
            messagebox.showinfo("Success", "Status updated.")

        ttk.Button(popup, text="Save", command=save_update).pack(pady=10)

    # -----------------------------------------------------------
    # TAB 3: ADD FORM
    # -----------------------------------------------------------
    def setup_add_form(self):
        form_frame = ttk.Frame(self.tab_add, padding=20)
        form_frame.pack(fill="both")

        def create_field(label_text, row):
            ttk.Label(form_frame, text=label_text).grid(row=row, column=0, sticky="w", pady=5)
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=row, column=1, sticky="w", pady=5)
            return entry

        self.ent_company = create_field("Company:", 0)
        self.ent_role = create_field("Role:", 1)
        
        self.ent_date = create_field("Date (YYYY-MM-DD):", 2)
        self.ent_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(form_frame, text="Status:").grid(row=3, column=0, sticky="w", pady=5)
        self.combo_status = ttk.Combobox(form_frame, values=VALID_STATUSES, state="readonly")
        self.combo_status.current(0)
        self.combo_status.grid(row=3, column=1, sticky="w", pady=5)

        ttk.Label(form_frame, text="Priority (1-5):").grid(row=4, column=0, sticky="w", pady=5)
        self.scale_priority = tk.Scale(form_frame, from_=1, to=5, orient="horizontal")
        self.scale_priority.set(3)
        self.scale_priority.grid(row=4, column=1, sticky="w", pady=5)

        ttk.Button(form_frame, text="Save Application", command=self.save_application).grid(row=5, column=1, sticky="e", pady=20)

    def save_application(self):
        company = self.ent_company.get().strip()
        role = self.ent_role.get().strip()
        date = self.ent_date.get().strip()
        status = self.combo_status.get()
        priority = self.scale_priority.get()

        if not company or not role:
            messagebox.showerror("Error", "Company and Role are required.")
            return

        sql = "INSERT INTO applications (company, role, date_applied, status, priority) VALUES (?, ?, ?, ?, ?)"
        self.db.execute_write(sql, (company, role, date, status, priority))
        
        messagebox.showinfo("Success", "Application Logged!")
        self.ent_company.delete(0, tk.END)
        self.ent_role.delete(0, tk.END)

    def on_tab_change(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if "Dashboard" in tab_text:
            self.refresh_dashboard()
        elif "List" in tab_text:
            self.refresh_list()

if __name__ == "__main__":
    app = SolSearchApp()
    app.mainloop()