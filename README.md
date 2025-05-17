# AI-summarizer

A full-stack AI-powered text summarizer web application.

---

## Features

- Upload txt or pdf files, or enter text directly
- Use any AI provider by configuring API URL, API key, model, temperature, and optional prompt
- Summarize text with OpenAI GPT or compatible APIs
- Store summaries in MongoDB and view recent summary history
- Vanilla JS + HTML + CSS frontend with modern UI
- FastAPI backend with asynchronous calls and file parsing
- Easy deployment with Render.com and CI/CD via GitHub Actions

---

## Setup Instructions

### Prerequisites

- Python 3.9+
- MongoDB Atlas or local MongoDB instance
- OpenAI API key or compatible AI provider API key

### Backend Setup

1. Navigate to `backend` folder:
 ```bash
 cd backend
 ```

Create and activate virtual environment:

```bash
python -m venv venv
```

To activate virtual environment :

On mac :

```bash
source venv/bin/activate
```
On Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```
Create .env file (or copy .env.example) and fill in your MongoDB URI and optional default OpenAI API details.

Run backend server:

```bash
uvicorn backend.main:app --reload
```

Server runs on http://localhost:8000.

#Frontend Setup
Open `frontend/index.html` in your browser directly or use a simple static server.

Update API URL in `script.js` if backend is not localhost.

Using the App
Enter or paste text or upload a `.txt` or `.pdf` file.

Enter your AI API URL, API Key, and model (e.g., gpt-3.5-turbo).

Adjust temperature and prompt if desired.

Click Summarize Text to get summary.

View recent summaries in history section.

Deployment & CI/CD
Push your backend to GitHub repo.

Connect repo to Render.com, set environment variables.

Use GitHub Actions workflow to auto deploy on push.

Notes
This app currently supports OpenAI Chat Completions API format.

File uploads are stored temporarily on server, not persisted.

You can extend this with user authentication and persistent file storage.
