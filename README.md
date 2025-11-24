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

  <h3 align="center">SolSearch</h3>

  <p align="center">
    The Professional, CLI-Based Job Application Tracker
    <br />
    <br />
    <a href="https://github.com/chiMsyt/FINALS_SOLSEARCH"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/chiMsyt/FINALS_SOLSEARCH/issues">Report Bug</a>
    ·
    <a href="https://github.com/chiMsyt/FINALS_SOLSEARCH/issues">Request Feature</a>
  </p>
</div>

<!-- BADGES -->
<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)]()
[![Database](https://img.shields.io/badge/SQLite-Integrated-07405E?logo=sqlite&logoColor=white)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

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
    <li><a href="#usage">Usage</a></li>
    <li><a href="#data-analytics">Data Analytics</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

---

## 📖 About The Project

**SolSearch** is a robust, terminal-based utility designed to help students and professionals organize the chaotic process of job hunting.

Managing 50+ job applications in spreadsheets is error-prone and tedious. SolSearch solves this by offering a **persistent database solution** that not only stores your application history but **analyzes it**. It provides actionable insights into your "Job Hunt Funnel," tracks your interest levels (Priority), and visualizes your progress with automatically generated charts.

It was built as a final capstone project for **DSA 214**, demonstrating core software engineering principles:
*   **Modularity** (Separation of Concerns)
*   **Security** (SQL Injection Prevention)
*   **Data Persistence** (Local Database)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### 🔧 Built With

*   ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
*   ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
*   ![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## ✨ Key Features

### 🔐 Secure Architecture
*   **Local Persistence:** Uses `SQLite3` to store data locally. No internet required.
*   **Security First:** Strict adherence to **Parameterized Queries** to prevent SQL Injection attacks.

### 📊 Analytics Engine
*   **Funnel Reports:** Calculates conversion rates (Application &rarr; Interview &rarr; Offer).
*   **Descriptive Stats:** Calculates Mean/Median priority scores to measure application quality.
*   **Visualization:** Auto-generates `.png` Bar Charts for visual reporting.

### 🖥️ Robust Interface
*   **Dynamic Sorting:** Sort history by ID, Company, Status, or Priority.
*   **Smart Formatting:** Automatic text truncation ensures tables never break layout.
*   **Visual Ratings:** Converts integer priorities into Star Ratings (⭐⭐⭐⭐⭐).

### 💾 Data Portability
*   **CSV Export:** One-click export to migrate data to Excel or Google Sheets.

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
4.  **Run the App**
    ```sh
    python main.py
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 🎮 Usage

### Generating Test Data
To demo the analytics without typing 50 entries manually, run the included seeder script.
```sh
python seed_data.py
```
> *Prompts you to wipe the DB and generates 50-100 realistic, weighted job entries.*

### Menu Controls

| Option | Action | Description |
| :--- | :--- | :--- |
| **1** | `Add` | Log a new job entry. |
| **2** | `View` | View history table. **Sortable** by ID, Status, or Priority. |
| **3** | `Update` | Move a job from 'Applied' to 'Interview', etc. |
| **4** | `Delete` | Remove an application by ID. |
| **5** | `Analyze` | View statistics and generate charts. |
| **6** | `Export` | Save database to `.csv` file. |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 📈 Data Analytics

SolSearch includes a dedicated `AnalyticsEngine` that transforms raw rows into insight.

**1. The Funnel Report**
> Automatically groups your applications to show where you stand.
> *   *Example: Applied (60%), Rejected (30%), Interview (10%)*

**2. Priority Alignment**
> Calculates the Median priority of your applications.
> *   *Insight: Are you applying for jobs you actually want?*

**3. Automatic Visualization**
> The system uses `matplotlib` to save a distribution chart to your project folder (`solsearch_analytics.png`).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## 👤 Contact

**Tim** - [GitHub Profile](https://github.com/chiMsyt)

Project Link: [https://github.com/chiMsyt/FINALS_SOLSEARCH](https://github.com/chiMsyt/FINALS_SOLSEARCH)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
