# AIStoryGenerator
A LLM-powered story generator which dynamically create options for you to choose your own adventure. Enter any theme, and the Cloudflare Workers AI (Llama 3.3 70B) will generate a multi-path narrative with winning endings.

Followed this [tutorial](https://www.youtube.com/watch?v=_1P0Uqk50Ps)

--- 

## Tech Stack
**Frontend** : React, Vite, React Router, Axios
**Backend:** FastAPI, Uvicorn, SQLAlchemy, Pydantic v2
**AI / LLM:** LangChain, Cloudflare Workers AI (`@cf/meta/llama-3.3-70b-instruct-fp8-fast`)
**Database:** SQLite (default) / PostgreSQL compatible

--- 

## Prerequisites
Before running the project, make sure you have:

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/) & `npm`
- [Git](https://git-scm.com/)
- A **Cloudflare Account** with access to Workers AI (Account ID and API Token)

---

## Backend Setup
Set up your backend, keep the AI running

### 1. Clone the Repository
```bash
git clone https://github.com/bikmet/AIStoryGenerator.git
cd AIStoryGenerator

```

### 2. Navigate to the backend directory
```bash
cd backend
```

### 3. Create and activate a virtual environment
Windows (PowerShell):
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```
macOS / Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### 4. Install required Python packages:
```bash
pip install -r requirements.txt
```

### 5. Create an environment configuration file:
```
API_PREFIX=/api
DEBUG=True

# Database connection string
DATABASE_URL=sqlite:///./stories.db

# CORS Allowed Origins (Comma-separated, strictly no trailing spaces)
ALLOWED_ORIGINS=http://localhost:5173,[http://127.0.0.1:5173](http://127.0.0.1:5173),http://localhost:3000

# Cloudflare Workers AI Configuration
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id_here
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token_here

# Optional (if required by Settings schema)
OPENAI_API_KEY=dummy_or_real_key
```

### 6. Run the FastAPI development:
```
python -u main.py
```
 ---
 
## Frontend Setup
Show the interface

### 1. Open a new terminal window/tab and navigate to the frontend folder:
```
cd frontend
```

### 2. Install the frontend dependencies:
```
npm install
```

### 3. Start the frontend development server
```
npm run dev
```

---

##How to use

- Open your browser and go to http://localhost:5173.

- Enter any genre, plot, or scenario prompt (e.g., "Cyberpunk Heist in Neo-Tokyo" or "Lost astronaut on a crystal planet").

- Click submit and wait while the AI crafts the branching tree nodes and options.

- Play through your story by clicking your decisions at every step!

## Notes & Troubleshooting

- CORS Errors: If you see CORS warnings in the browser console, double-check your backend/.env. Ensure ALLOWED_ORIGINS includes http://localhost:5173 without any spaces around the commas.

- Workers AI Model Limits: This project uses @cf/meta/llama-3.3-70b-instruct-fp8-fast. Ensure your Cloudflare API token has the Workers AI: Read permission enabled.

