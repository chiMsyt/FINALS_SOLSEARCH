import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import sys
import csv

DB_NAME = "solsearch.db"
VALID_STATUSES = ["Applied", "Interview", "Rejected", "Offer"]

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
        
        self.title("SolSearch - Job Application Tracker v2.0")
        self.geometry("1200x900") 
        
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        
        style = ttk.Style(self)
        style.theme_use('clam')

        # --- HEADER (ASCII LOGO + BUTTONS) ---
        header_frame = tk.Frame(self, bg="#2c3e50", height=160)
        header_frame.pack(fill="x")
        
        header_frame.columnconfigure(0, weight=1) # Center spacer
        
        lbl_logo = tk.Label(
            header_frame, 
            text=LOGO_TEXT, 
            font=("Courier", 10, "bold"), 
            fg="white", 
            bg="#2c3e50",
            justify="left"
        )
        lbl_logo.pack(side="left", padx=20, pady=10)

        # BUTTON CONTAINER
        btn_container = tk.Frame(header_frame, bg="#2c3e50")
        btn_container.pack(side="right", padx=20, pady=10)

        # EXPORT BUTTON
        btn_export = tk.Button(
            btn_container,
            text="[V] EXPORT CSV",
            font=("Arial", 10, "bold"),
            bg="#27ae60", # Green
            fg="white",
            activebackground="#2ecc71",
            activeforeground="white",
            command=self.export_to_csv,
            width=15,
            height=2
        )
        btn_export.pack(side="left", padx=5)

        # EXIT BUTTON
        btn_exit = tk.Button(
            btn_container, 
            text="[X] EXIT APP", 
            font=("Arial", 10, "bold"),
            bg="#c0392b", # Red
            fg="white",
            activebackground="#e74c3c",
            activeforeground="white",
            command=self.close_app,
            width=15,
            height=2
        )
        btn_exit.pack(side="left", padx=5)
        
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
    # SYSTEM UTILS
    # -----------------------------------------------------------
    def close_app(self):
        if messagebox.askokcancel("Exit", "Close SolSearch?"):
            plt.close('all')
            self.quit()
            self.destroy()
            sys.exit()

    def export_to_csv(self):
        rows = self.db.fetch_all("SELECT * FROM applications")
        if not rows:
            messagebox.showwarning("Export", "No data to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Export"
        )

        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Company", "Role", "Date Applied", "Status", "Priority"])
                    writer.writerows(rows)
                messagebox.showinfo("Success", f"Data exported to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    # -----------------------------------------------------------
    # TAB 1: DASHBOARD (Enhanced)
    # -----------------------------------------------------------
    def setup_dashboard(self):
        # Text Stats Frame
        self.stats_frame = ttk.Frame(self.tab_dashboard)
        self.stats_frame.pack(fill="x", pady=15, padx=10)
        
        # Helper for styled labels
        def make_stat_label(parent, text, color="black"):
            lbl = ttk.Label(parent, text=text, font=("Arial", 12, "bold"), foreground=color)
            lbl.pack(side="left", padx=15)
            return lbl

        self.lbl_total = make_stat_label(self.stats_frame, "Total: 0")
        self.lbl_active = make_stat_label(self.stats_frame, "Interviews: 0", "#2980b9") # Blue
        self.lbl_offers = make_stat_label(self.stats_frame, "Offers: 0", "#27ae60")    # Green
        self.lbl_rates = make_stat_label(self.stats_frame, "Response Rate: 0%", "#8e44ad") # Purple

        # Chart Frame (Holds Matplotlib canvas)
        self.chart_frame = ttk.Frame(self.tab_dashboard)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.canvas = None

    def refresh_dashboard(self):
        rows = self.db.fetch_all("SELECT status, priority FROM applications")
        total = len(rows)
        
        if total == 0:
            self.lbl_total.config(text="Total Apps: 0")
            if self.canvas: self.canvas.get_tk_widget().destroy()
            return

        # --- DATA PROCESSING ---
        statuses = [r[0] for r in rows]
        priorities = [r[1] for r in rows]

        count_interview = statuses.count("Interview")
        count_offer = statuses.count("Offer")
        count_rejected = statuses.count("Rejected")
        count_applied = statuses.count("Applied")
        
        # Analytics Calculations
        response_rate = ((count_interview + count_offer) / total) * 100
        
        # Update Text Labels
        self.lbl_total.config(text=f"Total: {total}")
        self.lbl_active.config(text=f"Interviews: {count_interview}")
        self.lbl_offers.config(text=f"Offers: {count_offer}")
        self.lbl_rates.config(text=f"Response Rate: {response_rate:.1f}%")

        # --- VISUALIZATION ---
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Create 1 figure with 2 subplots (Side by Side)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), dpi=100)
        fig.subplots_adjust(wspace=0.3)

        # Chart 1: Status Distribution (Pie Chart)
        labels = ["Applied", "Interview", "Offer", "Rejected"]
        sizes = [count_applied, count_interview, count_offer, count_rejected]
        colors = ['#95a5a6', '#3498db', '#2ecc71', '#e74c3c'] # Grey, Blue, Green, Red
        
        # Filter out zero values for cleaner chart
        clean_labels = []
        clean_sizes = []
        clean_colors = []
        for i, size in enumerate(sizes):
            if size > 0:
                clean_labels.append(labels[i])
                clean_sizes.append(size)
                clean_colors.append(colors[i])

        ax1.pie(clean_sizes, labels=clean_labels, colors=clean_colors, autopct='%1.1f%%', startangle=140)
        ax1.set_title("Status Distribution")

        # Chart 2: Priority Distribution (Bar Chart)
        priority_counts = {1:0, 2:0, 3:0, 4:0, 5:0}
        for p in priorities:
            if p in priority_counts:
                priority_counts[p] += 1
        
        p_x = list(priority_counts.keys())
        p_y = list(priority_counts.values())
        
        ax2.bar(p_x, p_y, color='#f1c40f', edgecolor='grey')
        ax2.set_title("Apps by Priority Level")
        ax2.set_xlabel("Priority (Stars)")
        ax2.set_ylabel("Count")
        ax2.set_xticks([1, 2, 3, 4, 5])
        ax2.grid(axis='y', linestyle='--', alpha=0.5)

        # Draw
        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # -----------------------------------------------------------
    # TAB 2: LIST VIEW
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
        
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=50)
        self.tree.heading("Company", text="Company")
        self.tree.column("Company", width=200)
        self.tree.heading("Role", text="Role")
        self.tree.column("Role", width=200)
        self.tree.heading("Date", text="Date")
        self.tree.column("Date", width=100)
        self.tree.heading("Status", text="Status")
        self.tree.column("Status", width=100)
        self.tree.heading("Priority", text="Priority")
        self.tree.column("Priority", width=100)

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