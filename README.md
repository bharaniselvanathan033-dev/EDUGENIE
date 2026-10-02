# EduGenie: Google Gemini Powered Learning Assistant

EduGenie is an AI-powered learning companion that helps students ask questions, understand difficult concepts, generate quizzes, summarize notes, and build personalized learning paths.

## Features

1. **AI Question & Answer** — Ask any study question and get a clear, structured AI answer
2. **Simple Concept Explanation** — Break down difficult concepts with analogies and key points
3. **Quiz Generator** — Auto-generate multiple-choice quizzes with answer checking and explanations
4. **Educational Text Summarizer** — Paste notes and get a concise summary with key takeaways
5. **Personalized Learning Path** — Get a step-by-step study plan with free resources
6. **Student Dashboard** — Clean dashboard with navigation between all features
7. **Study History** — Sessions are saved so you can revisit past results
8. **Responsive Design** — Works on desktop and mobile
9. **Offline Fallback** — If the backend is not running, the app uses a built-in knowledge engine

## Architecture

```
EduGenie-AI/
├── src/                    # Frontend (React + TypeScript + Tailwind CSS)
│   ├── App.tsx             # Main app with sidebar navigation and routing
│   ├── components/         # UI components (Dashboard, FeatureView, ResultCard, etc.)
│   └── lib/
│       ├── api.ts          # API client — calls backend, falls back to offline engine
│       ├── knowledgeEngine.ts  # Built-in offline knowledge engine (fallback)
│       └── supabase.ts     # Supabase client for study history
├── backend/
│   ├── main.py             # FastAPI backend with Gemini API integration
│   └── .env.example        # Backend environment variable template
├── supabase/               # Database migrations
├── requirements.txt        # Python dependencies
├── .env.example            # Frontend + backend env variable template
└── README.md               # This file
```

- **Frontend:** React + TypeScript + Tailwind CSS (Vite)
- **Backend:** Python FastAPI
- **AI:** Google Gemini API (gemini-1.5-flash)
- **Database:** Supabase (stores study history)

## Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- A free Google Gemini API key (get one at https://aistudio.google.com/apikey)

## Setup & Running

### 1. Frontend

```bash
npm install
npm run dev
```

The frontend runs at `http://localhost:5173`.

### 2. Backend (for Gemini AI features)

```bash
cd backend
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r ../requirements.txt
```

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `backend/.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

Start the backend:

```bash
python main.py
```

The backend runs at `http://localhost:8000`.

### 3. Connect Frontend to Backend

Create a `.env` file in the project root (if not already present) and add:

```
VITE_API_BASE_URL=http://localhost:8000
```

Restart the frontend if it was already running.

## API Endpoints

| Method | Endpoint              | Description                        |
|--------|-----------------------|------------------------------------|
| GET    | `/api/health`         | Health check + Gemini status       |
| POST   | `/api/qa`             | AI Question & Answer               |
| POST   | `/api/explain`        | Explain a concept                  |
| POST   | `/api/quiz`           | Generate a quiz                    |
| POST   | `/api/summarize`      | Summarize text                     |
| POST   | `/api/learning-path`  | Build a learning path              |

## Environment Variables

### Backend (`backend/.env`)

| Variable          | Required | Description                        |
|-------------------|----------|------------------------------------|
| `GEMINI_API_KEY`  | Yes      | Google Gemini API key              |
| `GEMINI_MODEL`    | No       | Model name (default: gemini-1.5-flash) |
| `ALLOWED_ORIGINS` | No       | CORS origins (default: *)          |

### Frontend (`.env`)

| Variable              | Required | Description                          |
|-----------------------|----------|--------------------------------------|
| `VITE_API_BASE_URL`   | No       | Backend URL (default: localhost:8000) |
| `VITE_SUPABASE_URL`   | Auto     | Supabase project URL (pre-configured) |
| `VITE_SUPABASE_ANON_KEY` | Auto  | Supabase anon key (pre-configured)   |

## Building for Production

```bash
npm run build
```

Output is in the `dist/` folder. Deploy to any static host (Netlify, Vercel, GitHub Pages, etc.).

For the backend, deploy to any Python host (Render, Railway, Fly.io, etc.) and set the `GEMINI_API_KEY` environment variable.

## Security

- The Gemini API key is stored only in the backend `.env` file and is never exposed to the frontend
- The `.env` file is listed in `.gitignore` and will not be committed
- The frontend communicates with the backend via HTTP requests — no API keys in browser code

## Offline Mode

If the Python backend is not running or the Gemini API key is not configured, EduGenie automatically falls back to a built-in offline knowledge engine. This means the app always works — you just get AI-powered responses when the backend is connected.

## Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Frontend | React 18, TypeScript, Tailwind CSS  |
| Build    | Vite 5                              |
| Backend  | Python, FastAPI, Uvicorn            |
| AI       | Google Gemini API (gemini-1.5-flash)|
| Database | Supabase (PostgreSQL)               |
| Icons    | lucide-react                        |
| Fonts    | DM Sans, Space Grotesk              |
