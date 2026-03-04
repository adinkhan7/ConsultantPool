# Consultant Pool

A live web app for searching, filtering, and managing your consultant database. Built with Flask + vanilla JS.

## Features
- Search by name, expertise, or location
- Filter by expertise, location, hourly rate range, and availability
- Sort by any column
- Add new consultants via a form
- Data persists in a local JSON file

## Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/consultant-pool.git
cd consultant-pool

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open http://localhost:5000 in your browser.

## Deploy to Render (Free)

1. Push this repo to GitHub
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment:** Python 3
5. Click Deploy

Your app will be live at `https://your-app-name.onrender.com`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/consultants` | List all consultants |
| POST | `/api/consultants` | Add a new consultant |
| PUT | `/api/consultants/<id>` | Update a consultant |
| DELETE | `/api/consultants/<id>` | Delete a consultant |

## Project Structure

```
consultant-pool/
├── app.py               # Flask backend + API
├── templates/
│   └── index.html       # Frontend UI
├── data/
│   └── consultants.json # Auto-created on first run
├── requirements.txt
├── Procfile             # For Render/Heroku deployment
└── .gitignore
```
