# 🚀 SolSearch Development Roadmap

## 📦 Phase 1: SolSearch v3.0 (Immediate Implementation)

### 🎯 Project Goal
> My primary goal for SolSearch v3.0 is to transition the application from a basic logger into a robust management tool. This update focuses on improving data interactivity, modernizing the user interface, and establishing a professional software architecture.

### 1. Functional Logic & Interactivity
*I need to make the data easier to manipulate and expand the depth of information I track for each application.*

- [ ] **Advanced Search & Filtering**
  - **Search Bar:** Implement entry field above list view.
    - *Logic:* `SELECT * FROM applications WHERE company LIKE ?` (Wildcard support).
  - **Salary Filtering:** Add logic to filter list based on pay ranges (e.g., *"Show > $100k"*).
- [ ] **Comprehensive Editing**
  - Bind a **Double-Click** event to Treeview rows.
  - Action: Open pre-filled "Edit Details" popup to fix typos or update Status without deleting the entry.
- [ ] **Integrated Date Picker**
  - Replace text entry with `tkcalendar`.
  - Action: Clicking the date field opens an interactive calendar widget.
- [ ] **Expanded Data Schema**
  - I will add the following columns to the database:

| Column Name      | Purpose                                          | Example                  |
| :--------------- | :----------------------------------------------- | :----------------------- |
| `notes`          | Job Description URLs or specific interview notes | *"Need to learn Docker"* |
| `salary`         | Offer amounts or salary ranges                   | `"$120k"`                |
| `resume_version` | Track exactly which resume file was used         | `"Data_CV_v2"`           |

### 2. GUI Aesthetics & User Experience
*I plan to replace the standard "Windows 95" look with a modern, professional interface.*

- [ ] **Modern Theming**
  - Refactor to use `ttkbootstrap` (Theme: **"Superhero"**).
  - *Goal:* Dark mode, flat buttons, and modern fonts with one line of code.
- [ ] **Theme Persistence**
  - Create `settings.json` to remember "Dark" or "Light" mode preference so it doesn't reset on restart.
- [ ] **Pagination**
  - Limit list view to **50 items per page** with "Next/Prev" buttons to handle 1,000+ seed entries.
- [ ] **Conditional Row Coloring**
  - Configure Treeview tags to automatically color-code rows:

| Status        | Color   | Hex Code  |
| :------------ | :------ | :-------- |
| **Offer**     | 🟢 Green | `#2ecc71` |
| **Rejected**  | 🔴 Red   | `#e74c3c` |
| **Interview** | 🔵 Blue  | `#3498db` |
| **Applied**   | ⚪ White | `Default` |

### 3. Advanced Analytics & Dashboard
*I want to derive deeper insights from my data to manage burnout and strategy.*

- [ ] **Application Velocity Chart**
  - **Type:** Line Graph.
  - **Insight:** "Applications Submitted Per Week" to track productivity and burnout trends.
- [ ] **Resume Performance (A/B Testing)**
  - **Type:** Bar Chart.
  - **Insight:** Compare Response Rates of "Resume V1" vs. "Resume V2".
- [ ] **Upcoming Interviews Widget**
  - **Logic:** Filter and display entries where `status = 'Interview'` **AND** `date > today`.

### 4. Testing & Simulation Data
*To properly test these new features, I need richer dummy data.*

- [ ] **Salary Generation:** Update `seed_data.py` to generate random salary ranges (e.g., *$60,000 - $150,000*).
- [ ] **Future Dates:** Update seeder so "Interviews" can have dates in the future (testing the Upcoming Widget).
- [ ] **Timeline Trends:** Modify date generation to create "spikes" (e.g., 3x more apps in September) to make the Velocity Chart look realistic.

### 5. Backend Architecture
*I need to pay off technical debt and prepare the codebase for scalability.*

- [ ] **Schema Migration Script**
  - Write a Python script to append `notes`, `salary`, and `resume_version` to the existing `solsearch.db` without deleting current data.
- [ ] **ORM Implementation (SQLAlchemy)**
  - Move from raw `sqlite3` to **SQLAlchemy**.
  - *Benefit:* Cleaner code, easier management of complex filtering queries, and professional architecture.

---

## 🔮 Phase 2: SolSearch v4.0 & Beyond (Future Vision)

### 🌌 Project Vision: The Career Management Suite
> My vision for SolSearch v4.0 is to evolve the application from a passive application tracker into a proactive **Career Management Suite**. By integrating automation, AI, and relational data structures, I aim to reduce the manual friction of job hunting while providing strategic advantages during the interview process.

### 1. Intelligent Automation & AI Integration
*My goal is to minimize manual data entry and leverage LLMs.*

- **AI-Powered "Career Copilot"** (Llama 3 / OpenAI)
  - **Resume Optimization:** Compare stored resume text against a Job Description to highlight missing keywords (e.g., *"Missing: Agile, Docker"*).
  - **Cover Letter Generator:** Automatically draft tailored letters based on Company and Role data.
- **Web Scraper / URL Parser**
  - Paste LinkedIn/Indeed URLs to auto-fill "Company", "Role", and "JD" using `BeautifulSoup` or `selenium`.
- **Email Inbox Parser ("Lazy Mode")**
  - Connect to Gmail API (Read-Only).
  - Scan for "Application Received" emails, extract company names, and auto-create entries.

### 2. Advanced Workflow & Visualization
*Moving beyond list views for better spatial and temporal understanding.*

- **Kanban Board Visualization**
  - "Trello-style" drag-and-drop columns (Applied $\to$ Interview $\to$ Offer $\to$ Rejected).
- **Automated "To-Do" & Reminder System**
  - *Applied:* Auto-generate task $\to$ "Follow up in 7 days."
  - *Interview:* Auto-generate task $\to$ "Send Thank You note 1 day after."
- **Calendar Synchronization**
  - Push interview dates to Google Calendar (via `.ics` or API) with Zoom links included.

### 3. Comprehensive Data & Asset Management
*Centralizing people, documents, and context.*

- **Networking & Contacts System**
  - Relational DB table for `Contacts`. Link Recruiters (Name, Email, LinkedIn) to specific applications.
- **Job Description (JD) Archiving**
  - Text storage or file upload to save JDs locally, protecting against dead web links.
- **Document Handling**
  - Store file paths for the specific PDF Cover Letter and Resume used for each job (Single-click access).

### 4. Live Interview Support
*Tools for a competitive edge during the conversation.*

- **"Live Interview HUD" (Head-Up Display)**
  - Transparent "Always-on-Top" overlay for Zoom/Teams.
  - **Displays:** Interviewer Name, STAR Method stories, and Strategic Questions to ask.

### 5. Motivation & Market Insights
*Features to maintain morale and provide leverage.*

- **Market Salary Comparison**
  - Integrate Glassdoor/Levels.fyi APIs for real-time median salary data context during negotiation.
- **Gamification & Achievements**
  - "Stats & Trophies" profile with badges:
    - 🏆 *The Grinder:* Applied to 10 jobs in 1 day.
    - 👻 *Ghostbuster:* Followed up on 5 ghosted applications.
    - 🔥 *Level Up:* Current Streak: 7 days.

### 6. Security & Reliability
*Protecting sensitive career data.*

- **Encryption & Privacy Mode**
  - Implement **SQLCipher** with a master password to protect notes, salary data, and contacts.
- **Cloud Backup & Export**
  - Export DB to JSON or sync to secure cloud (Firebase/Supabase) to prevent data loss from hardware failure.