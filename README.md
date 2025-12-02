<a name="readme-top"></a>

<div align="center">

  <!-- ASCII ART LOGO -->
  <pre>
   _____       __ _____                     __     
  / ___/____  / // ___/___  ____ __________/ /_    
  \__ \/ __ \/ /\__ \/ _ \/ __ `/ ___/ ___/ __ \   
 ___/ / /_/ / /___/ /  __/ /_/ / /  / /__/ / / /   
/____/\____/_//____/\___/\__,_/_/   \___/_/ /_/    
        :: Career Tracking System v2.0 ::          
  </pre>

  <h3 align="center">SolSearch v2.0</h3>

  <p align="center">
    A Professional, GUI-Based Job Application Tracker & Analytics Engine.
    <br />
    <br />
    <a href="implementations.md"><strong>View Roadmap (v3.0 & v4.0) »</strong></a>
    <br />
    <br />
    <a href="https://github.com/chiMsyt/FINALS_SOLSEARCH/issues">Report Bug</a>
    ·
    <a href="https://github.com/chiMsyt/FINALS_SOLSEARCH/issues">Request Feature</a>
  </p>
</div>

<!-- BADGES -->
<div align="center">

[![Status](https://img.shields.io/badge/Status-v2.0_Stable-success?style=flat&logo=git)]()
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python&logoColor=white)]()
[![GUI](https://img.shields.io/badge/Interface-Tkinter-orange?style=flat&logo=tcl&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)]()

</div>

<br />

<!-- TABLE OF CONTENTS -->
<details>
  <summary><strong>Table of Contents</strong> (Click to Expand)</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#key-features">Key Features</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage-guide">Usage Guide</a></li>
    <li><a href="#development-roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

---

## 📖 About The Project

**SolSearch** is a robust desktop utility designed to organize the chaotic process of job hunting.

Managing hundreds of job applications in spreadsheets is error-prone and provides zero insight. SolSearch solves this by offering a **persistent database solution** wrapped in a user-friendly GUI. It not only stores your application history but **analyzes it** in real-time, visualizing your "Job Hunt Funnel" and priority distribution.

This project serves as a final capstone for **DSA 214**, demonstrating:
*   **Object-Oriented Design:** Modular `DatabaseManager` and `UserInterface` classes.
*   **Data Persistence:** SQLite integration for reliable local storage.
*   **Data Visualization:** Embedded Matplotlib charts within a Tkinter window.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### 🔧 Built With

*   ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
*   ![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange?style=for-the-badge)
*   ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
*   ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## ✨ Key Features

### 🖥️ The v2.0 Dashboard
*   **Real-Time Metrics:** Instantly calculate Total Applications, Active Interviews, Offers, and Response Rates.
*   **Embedded Analytics:**
    *   **Pie Chart:** Visualizes the status breakdown (Applied vs. Rejected vs. Offer).
    *   **Bar Chart:** Analyzes your "Priority Alignment" (Are you applying to jobs you actually want?).

### 🗂️ Application Management
*   **List View:** A sortable table of all applications.
*   **CRUD Actions:**
    *   **Update:** Move candidates through the pipeline (e.g., `Applied` &rarr; `Interview`).
    *   **Delete:** Remove erroneous entries safely.
*   **Dynamic Sorting:** Sort by Company (A-Z), Status, ID, or Priority.

### 💾 Data & Security
*   **Local Persistence:** Zero-latency SQLite database. No internet connection required.
*   **CSV Export:** One-click backup to migrate data to Excel/Google Sheets.
*   **Safety:** Parameterized SQL queries prevent injection attacks.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 🚀 Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites
*   Python 3.8+
*   Pip

### Installation

1.  **Clone the repo**
    ```sh
    git clone https://github.com/chiMsyt/FINALS_SOLSEARCH.git
    ```
2.  **Navigate to the directory**
    ```sh
    cd FINALS_SOLSEARCH
    ```
3.  **Install dependencies**
    ```sh
    pip install matplotlib
    ```
    *(Note: `tkinter` and `sqlite3` are included with standard Python installations)*
4.  **Run the App**
    ```sh
    python main.py
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 🎮 Usage Guide

### 1. Generating Test Data
Don't want to type empty data? Run the seeder to populate the database with **1,000 realistic entries** from top companies (Google, Amazon, startups, etc.).
```sh
python seed_data.py
```

### 2. The Interface
The application is divided into three main tabs:

| Tab Name        | Functionality                                                                                      |
| :-------------- | :------------------------------------------------------------------------------------------------- |
| **📊 Dashboard** | View global statistics, Response Rate %, and Matplotlib charts.                                    |
| **📂 List View** | The main table. Click column headers to **Sort**. Select a row to **Update Status** or **Delete**. |
| **➕ Add New**   | Form to log a new application. Includes Priority Slider (1-5) and Date entry.                      |

### 3. Exporting
Click the **`[V] EXPORT CSV`** button in the top header to save your entire database to a `.csv` file for external analysis.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 🗺️ Development Roadmap

We are currently planning **v3.0** and **v4.0**. Full details can be found in [implementations.md](implementations.md).

*   **v3.0:** Dark Mode (`ttkbootstrap`), Search Bar, Salary Filtering, Resume Versioning.
*   **v4.0:** AI Resume Optimization, Kanban Boards, and Google Calendar Sync.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 👤 Contact

**Tim** - [GitHub Profile](https://github.com/chiMsyt)

Project Link: [https://github.com/chiMsyt/FINALS_SOLSEARCH](https://github.com/chiMsyt/FINALS_SOLSEARCH)

<p align="right">(<a href="#readme-top">back to top</a>)</p>