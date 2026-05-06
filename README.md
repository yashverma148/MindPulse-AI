<div align="center">

# 🧠 MindPulse AI

### _AI-Powered Behavioral Intelligence & Productivity Analytics Platform_

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Scikit--learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-CDN-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

MindPulse AI is a SaaS-level behavioral intelligence platform that combines machine learning, productivity analytics, and large language models (LLMs) to analyze real-world user behavior and generate actionable insights.

[🚀 Getting Started](#-getting-started) · [✨ Features](#-features) · [🧠 AI Architecture](#-ai-architecture) · [📡 API](#-api-endpoints) · [🛠️ Tech Stack](#️-tech-stack)

---

</div>

MindPulse AI is a production-ready SaaS platform designed to analyze digital behavior, productivity patterns, focus consistency, and browsing activity using Machine Learning and LLM-powered reasoning.

Unlike traditional productivity trackers, MindPulse AI transforms real behavioral data into actionable intelligence through:

- 📊 ML-based productivity scoring
- 🧠 LLM-generated behavioral insights
- 🧩 Custom-built Chrome Extension for browser intelligence
- 🔥 Habit streak analytics
- 📈 Real-time interactive visualizations
- 😈 AI-generated contextual feedback

> _"Not what you think you did — what your behavioral data proves."_

---

# 📄 Product Showcase

Explore the complete MindPulse AI SaaS interface, analytics system, AI insights engine, browser intelligence module, and productivity tracking workflow.

<p align="center">
  <a href="./static/images/MindPulse_AI_Organized_Showcase.pdf">
    <img src="https://img.shields.io/badge/View-Full_Product_Showcase_PDF-8A2BE2?style=for-the-badge&logo=adobeacrobatreader&logoColor=white"/>
  </a>
</p>


## ⚡ Why This Project?

Most productivity apps rely on manual tracking and static analytics.

MindPulse AI goes beyond that by combining:
- **Machine Learning** — Quantitative scoring through trained models
- **Behavioral Intelligence** — Pattern recognition across user activity
- **Self-Programmed Chrome Extension** — Custom-built extension for secure browsing data syncing & classification
- **LLM-based Reasoning** — Human-like contextual analysis and recommendations
- **Real-time Analytics** — Live charts, heatmaps, and streak tracking
- **SaaS-grade UI/UX** — Glassmorphism dark theme with micro-animations

This makes the platform behave more like an **intelligent productivity operating system** rather than a traditional dashboard application.

---

## ✨ Features

### 🎯 Core Productivity Engine
| Feature | Description |
|---|---|
| **📊 ML Productivity Scoring** | A trained **Random Forest Regressor** evaluates 8 engineered features from your daily input and outputs a **0–100 productivity score** in real-time. |
| **🤖 LLM-Powered Insights** | Uses an advanced LLM inference pipeline with multi-model fallback architecture to generate contextual summaries, behavioral analysis, productivity recommendations, and intelligent feedback in real time. |
| **🔥 Contextual Feedback Mode** | Toggle on "Roast Mode" for AI-generated sarcastic, context-aware commentary on your behavioral stats — powered by contextual prompt engineering. |
| **📈 Interactive Visualizations** | Real-time **Chart.js** visualizations — donut chart for time distribution, line chart for weekly productivity trends — all updating live without page reloads. |

### 🌐 Browser Activity Intelligence
| Feature | Description |
|---|---|
| **🧩 MindPulse Chrome Extension** | A secure, cloud-compatible browser extension that collects and syncs your browsing history securely to the backend via token-based authentication. |
| **🔍 Browsing History Analysis** | Classifies every synced visit as **Productive**, **Distraction**, or **Neutral** using a curated domain classification engine (supports both cloud-synced and local fallback modes). |
| **🏆 Top Sites Ranking** | See your top 10 most-visited sites with visit counts, color-coded by behavioral category. |
| **📊 Category Breakdown** | Visual donut chart showing the ratio of productive vs. distraction browsing patterns. |
| **⏱️ Time Range Filter** | Analyze browsing behavior for the last 24 hours, 3 days, or 7 days. |

### 🔥 Habit Streaks & Behavioral Heatmap
| Feature | Description |
|---|---|
| **🔢 Streak Tracker** | Tracks your current and longest consecutive logging streaks — behavioral consistency metric. |
| **📅 90-Day Activity Heatmap** | GitHub-style heatmap visualizing your activity over the last 90 days, color-coded by productivity score intensity. |
| **📊 Lifetime Stats** | Total logs, average score, and streak data aggregated for long-term trend analysis. |

### 🛡️ Data & Account Management
| Feature | Description |
|---|---|
| **🔐 Secure Auth** | User registration and login with **bcrypt password hashing** and Flask session management. |
| **📥 CSV Export** | Download your complete behavioral history as a `.csv` file for external analysis or data science workflows. |
| **🗑️ Data Clearing** | One-click option to permanently delete all activity logs from the database. |
| **📋 Reports Table** | Sortable history table with date, score, productive hours, distraction hours, and status indicators. |

### 🎨 Premium SaaS UI/UX
| Feature | Description |
|---|---|
| **🌙 Dark Mode Design** | A deep, immersive dark theme with ambient gradient backgrounds. |
| **✨ Glassmorphism** | Frosted glass panels and cards with `backdrop-filter: blur()` effects. |
| **🎭 Micro-Animations** | Smooth slide-in transitions, animated score counters, skeleton loading states, and hover interactions. |
| **📱 Multi-Tab Navigation** | Sidebar-driven SPA-like navigation across Dashboard, Insights, Reports, Settings, Chrome Analysis, and Habit Streaks tabs. |

---

## 🧠 AI Architecture

MindPulse AI uses a **hybrid intelligence architecture** that separates concerns across three distinct processing layers:

### 🔹 Machine Learning Layer
Responsible for:
- Productivity score prediction (Random Forest Regressor, 100 estimators)
- Feature engineering (productivity ratio, distraction ratio, consistency score)
- Behavioral pattern quantification
- Statistical productivity analysis on synthetic + real user data

### 🔹 LLM Intelligence Layer
Responsible for:
- Natural language reasoning over behavioral metrics
- Contextual behavioral interpretation
- Context-aware personalized recommendations
- Human-like productivity feedback generation
- Structured JSON response generation via prompt engineering
- Multi-model fallback architecture with retry handling

### 🔹 Behavioral Data Layer
Processes:
- Productivity metrics (study, work, screen time, sleep)
- Browsing activity classification (30+ productive & distraction domains)
- Distraction pattern analysis
- Habit consistency & streak computation
- User interaction history & trend aggregation

> This layered architecture allows the platform to combine **statistical ML predictions** with **contextual AI reasoning** — producing insights that are both data-driven and human-interpretable.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser)                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │Dashboard │  │ Insights │  │ Reports  │  │Chrome Analysis │  │
│  │  Tab     │  │   Tab    │  │   Tab    │  │     Tab        │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───────┬────────┘  │
│       │              │             │                │            │
│  ┌────┴──────────────┴─────────────┴────────────────┴────────┐  │
│  │              Vanilla JS (main.js) + Chart.js              │  │
│  │           TailwindCSS (CDN) + Custom CSS (styles.css)     │  │
│  └──────────────────────────┬────────────────────────────────┘  │
│                             │ REST API (JSON)                    │
│  ┌──────────────────────────┴────────────────────────────────┐   │
│  │                  CHROME EXTENSION                         │   │
│  │  (Background Service Worker + Secure Token Sync)          │   │
│  └──────────────────────────┬────────────────────────────────┘   │
└─────────────────────────────┼────────────────────────────────────┘
                              │ Secure API & Token Auth
┌─────────────────────────────┼────────────────────────────────────┐
│                     FLASK SERVER (app.py)                        │
│  ┌──────────────────────────┴────────────────────────────────┐   │
│  │                     Route Handlers                        │   │
│  │  /predict  /insights  /history  /streak  /chrome-history  │   │
│  │  /api/extension/sync  /login  /signup  /logout            │   │
│  └────────┬────────────────┬───────────────────┬─────────────┘   │
│           │                │                   │                 │
│  ┌────────▼──────┐  ┌──────▼──────────┐  ┌────▼──────────────┐ │
│  │  ML Engine    │  │ LLM Intelligence│  │ Browser Activity  │ │
│  │ (Random Forest│  │    Layer        │  │ Analyzer (Cloud   │ │
│  │  Regressor)   │  │ (Multi-Model    │  │ Sync + Local Fall-│ │
│  │               │  │  Fallback +     │  │ back Classifier)  │ │
│  │               │  │  Prompt Engine) │  │                   │ │
│  └───────────────┘  └────────────────-┘  └───────────────────┘ │
│           │                │                                   │
│  ┌────────▼────────────────▼──────────────────────────────┐    │
│  │              SQLite Database (site.db)                 │    │
│  │      Users  ←──one-to-many──→  DailyLogs / History     │    │
│  └────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔄 How It Works

### 1. 📝 Behavioral Data Input
The user enters daily behavioral metrics via interactive sliders on the Dashboard:
- **Study Hours** (0–16h)
- **Work Hours** (0–16h)
- **Screen Time** (0–24h)
- **Distraction Time** (0–12h)
- **Sleep Hours** (0–14h)

### 2. 🤖 ML Prediction Pipeline
When you click **"Generate Analysis"**, the backend performs feature engineering:

```python
productivity_ratio  = (study + work) / (screen_time + 0.1)
distraction_ratio   = distraction / (study + work + 0.1)
consistency_score   = sleep / 8.0
```

These 8 features are fed into the **Random Forest Regressor** (100 estimators, trained on 1000 synthetic samples) to predict a **0–100 productivity score**.

### 3. 🧠 LLM Behavioral Intelligence Layer

The productivity score and behavioral metrics are processed through an LLM-powered reasoning engine that generates:

- 📋 **Daily Productivity Summaries** — Contextual recap of the day
- 🧬 **Behavioral Pattern Analysis** — Deep pattern recognition across metrics
- 🎯 **Personalized Improvement Recommendations** — Actionable, data-driven suggestions
- 🔥 **Context-Aware Productivity Feedback** — Intelligent commentary (or sarcastic roast)

The inference layer uses:
- **Multi-model fallback architecture** — Automatic model switching on rate limits
- **Retry handling** — Exponential backoff with 10-second cooldowns
- **Structured JSON response generation** — Reliable, parseable output
- **Contextual prompt engineering** — Behavior-aware prompt construction

> This enables MindPulse AI to generate **human-like productivity analysis** instead of static rule-based feedback.

### 4. 📊 Real-Time Visualization & Tracking
- The **donut chart** updates live as you move sliders
- The **trend chart** plots your score history over time
- The **heatmap** shows your 90-day activity pattern
- **Streak counter** motivates daily logging consistency

### 5. 🌐 Browser Activity Intelligence (Optional)
MindPulse AI securely captures your browser activity using a dedicated **Chrome Extension**. It syncs the history securely to the backend where it classifies sites using a domain classification engine:

| Category | Example Sites |
|---|---|
| ✅ Productive | GitHub, StackOverflow, LeetCode, Coursera, Figma, Notion, HuggingFace |
| ❌ Distraction | YouTube, Netflix, Reddit, Instagram, Twitter/X, TikTok, Discord |
| ⚪ Neutral | Everything else |

*(Note: The system still supports a local SQLite fallback for users who prefer direct local file reading without the extension).*

---

## 📡 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/` | ✅ | Dashboard (redirects to login if not authenticated) |
| `GET` | `/login` | ❌ | Login page |
| `POST` | `/login` | ❌ | Authenticate user |
| `GET` | `/signup` | ❌ | Registration page |
| `POST` | `/signup` | ❌ | Create new account |
| `GET` | `/logout` | ✅ | End session |
| `POST` | `/predict` | ✅ | Submit behavioral data → ML prediction → returns `{score, log_id}` |
| `POST` | `/insights` | ✅ | Generate LLM insights for a log → returns `{summary, suggestions, behavioral_analysis, roast}` |
| `GET` | `/history` | ✅ | Fetch all user logs → returns `[{date, score, productive_time, distraction_time}]` |
| `GET` | `/export-csv` | ✅ | Download behavioral history as CSV file |
| `POST` | `/clear-logs` | ✅ | Delete all activity logs for current user |
| `GET` | `/chrome-history?hours=24` | ✅ | Analyze Chrome browsing activity for last N hours |
| `GET` | `/streak` | ✅ | Get streak stats + 90-day heatmap data |

---

## 🛠️ Tech Stack

<table>
<tr>
<td><b>Layer</b></td>
<td><b>Technology</b></td>
<td><b>Purpose</b></td>
</tr>
<tr>
<td>🖥️ Backend</td>
<td>Flask, Flask-SQLAlchemy, Flask-Bcrypt</td>
<td>Web server, ORM, password hashing</td>
</tr>
<tr>
<td>🎨 Frontend</td>
<td>HTML5, Vanilla JS, TailwindCSS (CDN), Chart.js</td>
<td>UI rendering, charts, SPA-like interactivity</td>
</tr>
<tr>
<td>🧠 AI Layer</td>
<td>LLM Inference Pipeline + Prompt Engineering</td>
<td>Behavioral reasoning, contextual feedback, multi-model fallback</td>
</tr>
<tr>
<td>📊 ML Layer</td>
<td>Scikit-learn, Pandas, NumPy, Joblib</td>
<td>Random Forest model training, feature engineering, inference</td>
</tr>
<tr>
<td>🗄️ Database</td>
<td>SQLite</td>
<td>User accounts & behavioral activity logs</td>
</tr>
<tr>
<td>🌐 Browser Intel</td>
<td>Chrome SQLite Reader + Domain Classifier</td>
<td>Browsing history analysis & site categorization</td>
</tr>
<tr>
<td>🔐 Security</td>
<td>Bcrypt + Flask Sessions</td>
<td>Secure password storage & session management</td>
</tr>
</table>

---

## 📁 Project Structure

```
MindPulse AI/
├── 📄 app.py                    # Flask application entry point & all route handlers
├── 📄 .env                      # Environment variables (SECRET_KEY, API keys)
├── 📄 README.md                 # You are here! 📍
│
├── 📂 database/
│   └── models.py                # SQLAlchemy models (User, DailyLog)
│
├── 📂 browser-extension/        # MindPulse Browser Intelligence Extension
│   ├── manifest.json            # Chrome extension configuration
│   ├── popup.html               # Extension popup UI
│   ├── popup.js                 # Extension popup logic (Token Sync)
│   ├── popup.css                # Extension styling
│   └── service_worker.js        # Background syncing logic
│
├── 📂 model/
│   └── rf_model.joblib          # Trained Random Forest model (~7MB)
│
├── 📂 utils/
│   ├── gemini_service.py        # LLM inference layer with multi-model fallback
│   ├── chrome_analyzer.py       # Browser activity reader & domain classifier
│   └── ml_pipeline.py           # Synthetic data generation & model training pipeline
│
├── 📂 data/
│   └── synthetic_data.csv       # Generated training dataset (1000 samples)
│
├── 📂 templates/
│   ├── base.html                # Base template (head, scripts, toast system)
│   ├── dashboard.html           # Main app UI (all 6 tabs)
│   ├── login.html               # Login page
│   └── signup.html              # Registration page
│
├── 📂 static/
│   ├── css/styles.css           # Custom styles (glassmorphism, animations, sliders)
│   ├── js/main.js               # Client-side logic (charts, tabs, API calls)
│   └── images/
│       ├── logo.jpg             # MindPulse AI brand logo
│       └── favicon.ico          # Browser tab icon
│
└── 📂 instance/
    └── site.db                  # SQLite database (auto-created on first run)
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed
- **Google Chrome** (optional — for Browser Activity Intelligence)
- **LLM API Key** — Required for the AI inference layer ([Get one free](https://aistudio.google.com/apikey))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/mindpulse-ai.git
cd mindpulse-ai

# 2. Create & activate virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_super_secure_random_key_here
GEMINI_API_KEY=your_llm_api_key_here
```

> 💡 **Tip**: Generate a secure key with `python -c "import secrets; print(secrets.token_hex(32))"`

### Train the ML Model

```bash
python utils/ml_pipeline.py
```
```
✅ Generating synthetic data...
✅ Data saved to data/synthetic_data.csv
✅ Training Random Forest model...
✅ Model trained with R² score: 0.95+
✅ Model saved to model/rf_model.joblib
```

### Run the Application

```bash
python app.py
```

🎉 Open **http://127.0.0.1:5000** in your browser and start tracking!

### Install the Chrome Extension (Optional)

To enable cloud-synced browser activity intelligence:
1. Open Google Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** in the top right corner.
3. Click **Load unpacked** and select the `browser-extension` folder in this repository.
4. Open the extension popup, log in if necessary, and it will sync your data securely.

---

## 🎮 Quick Start Guide

1. **Sign Up** → Create your account on the registration page
2. **Log In** → Enter your credentials
3. **Move the Sliders** → Set your study, work, screen time, distractions & sleep hours
4. **Generate Analysis** → Click the button to get your ML score + LLM-powered insights
5. **Explore Tabs** → Check out Insights, Reports, Chrome Analysis, and Habit Streaks
6. **Toggle Roast Mode** → Enable context-aware AI feedback for brutally honest commentary 🔥
7. **Export Data** → Download your behavioral history as CSV from the Reports tab

---

## 🔮 Roadmap

- [ ] 📧 Email verification for new accounts
- [ ] 📄 PDF report generation with embedded charts
- [ ] 💾 Offline mode with local storage caching
- [ ] 📱 Progressive Web App (PWA) support
- [ ] 🔗 Integration with Google Calendar & Todoist
- [ ] 📊 Weekly/Monthly automated summary reports
- [ ] 🧪 Expand ML model with real-world behavioral data
- [ ] 🌍 Multi-language support
- [ ] 🔌 Plugin architecture for custom data sources
- [ ] 📉 Anomaly detection in behavioral patterns

---

<div align="center">

### Built with ❤️ for productivity optimization

**MindPulse AI** — _Know yourself. Improve yourself. Roast yourself._ 🔥

AI-powered behavioral intelligence platform that combines Machine Learning, LLM-based reasoning, productivity analytics, and browser activity analysis to generate real-time insights, productivity scoring, habit tracking, and contextual AI feedback through a modern SaaS dashboard.

⭐ Star this repo if you found it useful!

</div>
