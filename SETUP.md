# Quick Setup Guide

## ⚡ 5-Minute Setup

### Step 1: Prerequisites
- ✅ Python 3.8+ installed
- ✅ PostgreSQL 12+ installed and running
- ✅ Google Gemini API key ([Get it free](https://makersuite.google.com/app/apikey))

### Step 2: Clone & Install
```bash
git clone <your-repo-url>
cd nl-database-search
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r req.txt
```

### Step 3: Configure
Create `.env` file:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vosco
DB_USER=postgres
DB_PASSWORD=your_password
GOOGLE_API_KEY=your_gemini_api_key
```

### Step 4: Setup Database
```bash
python db_setup.py
python insert_sample_data.py
```

### Step 5: Run
```bash
streamlit run app.py
```

Open browser: http://localhost:8501

## 🎯 Test Queries

Try these:
- "Show all employees"
- "What's the average salary by department?"
- "Find products under $100"

## 🐛 Common Issues

**Issue:** `ModuleNotFoundError`
**Fix:** Run `pip install -r req.txt`

**Issue:** Database connection error
**Fix:** Check PostgreSQL is running and `.env` is configured

**Issue:** Gemini API error
**Fix:** Verify your `GOOGLE_API_KEY` is valid

## 📚 More Info

- Full docs: [README.md](README.md)
- Architecture: [architecture.txt](architecture.txt)

---
**Happy querying! 🚀**
