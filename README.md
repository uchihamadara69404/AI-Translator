# Tarjama · ترجمة

An AI-powered web application that translates official English PDF documents into Arabic with full formatting preservation and independent dual-layer verification.
=======
Built for use cases involving sensitive, legal, or governmental content where translation accuracy is non-negotiable. Tarjama does not simply translate text — it runs a second independent AI verification pass that audits the translation and returns a structured accuracy report with a final verdict of **APPROVED**, **NEEDS REVISION**, or **REJECTED**.

---

## How It Works

**Step 1 — Format-Preserving Extraction**
The PDF is parsed using `pdfplumber` with layout mode enabled, which reconstructs document structure from the raw positional data of each text item. Paragraphs, bullet points, numbered lists, indentation, and multi-column structures are preserved as faithfully as possible.

**Step 2 — AI Translation**
The extracted text is sent to Groq's `llama-3.3-70b-versatile` model with a system prompt that instructs it to act as an expert translator for official documents and output only the Arabic translation with all formatting intact.

**Step 3 — Independent Dual-Layer Verification**
A second, completely separate API call is made using a different system prompt that frames the model as a senior bilingual Arabic-English auditor. This call receives both the original English and the translated Arabic and produces a structured audit report. The separation is intentional — having the same model validate its own output in a single call introduces self-validation bias. Two independent calls with opposing personas produce a more objective result.

**Step 4 — Structured Audit Report**
The verification report covers:
- Overall Accuracy Score (0–100%)
- Semantic Accuracy — whether meaning transfers correctly
- Contextual Fidelity — whether cultural and legal nuance is preserved
- Terminology Issues — any mistranslated or ambiguous terms
- Structural Integrity — whether the document layout survived translation
- Critical Errors — anything specifically wrong in sensitive content
- Final Verdict — APPROVED, NEEDS REVISION, or REJECTED with reasoning

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python + Flask |
| PDF parsing | pdfplumber (layout mode) |
| AI model | Groq llama-3.3-70b-versatile |
| Frontend | Plain HTML + CSS + vanilla JavaScript |
| Env management | python-dotenv |

---

## Architecture

```
Browser
  │
  ├── POST /upload   → pdfplumber extracts and preserves layout → returns plain text
  ├── POST /translate → Groq API (Translator persona) → returns Arabic translation
  └── POST /verify   → Groq API (Auditor persona) → returns structured audit report
```

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — for the Docker path
- Python 3.11+ — for the local path
- Free Groq API key from [console.groq.com](https://console.groq.com)

---

## Step 1 — Set Up Your API Key

Do this first regardless of which method you use.

```bash
cp .env.example .env
```

Open `.env` and replace `your-groq-api-key-here` with your actual key:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Never commit `.env` to git — it is already in `.gitignore`.

---

## Option A — Docker (Recommended)

No Python install needed. Docker handles everything.

```bash
# Build the image (first time takes 2–3 minutes)
docker build -t tarjama .

# Run
docker run --env-file .env -p 5000:5000 tarjama
```

Open **http://localhost:5000** in your browser.

**With Docker Compose:**
```bash
docker compose up      # start
docker compose down    # stop
```

**Pass key directly without .env:**
```bash
docker run -e GROQ_API_KEY=gsk_xxxxxxxxxxxx -p 5000:5000 tarjama
```

---

## Option B — Run Locally with Python

**Step 1 — Create a virtual environment**
```bash
python -m venv .venv

# Activate:
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows CMD
.venv\Scripts\Activate.ps1       # Windows PowerShell
```

**Step 2 — Install packages**
```bash
pip install -r requirements.txt
```

**Step 3 — Start the server**
```bash
python app.py
```

Open **http://localhost:5000**

---

## Option C — GitHub Codespaces

The repo includes a devcontainer that installs all dependencies automatically on launch.

1. Open the repo on GitHub
2. Click **Code → Codespaces → Create codespace on main**
3. Wait for the environment to build (about 1 minute)
4. Add your Groq key — either:
   - Set it as a Codespace secret: GitHub → Settings → Codespaces → Secrets → add `GROQ_API_KEY`
   - Or run in the terminal: `export GROQ_API_KEY=gsk_xxxxxxxxxxxx`
5. Start the server:
```bash
python app.py
```
6. A popup will appear to open port 5000 in your browser

---

## Using the App

1. Click **Upload PDF** and select an English PDF document
2. Click **Translate** — the Arabic translation appears in the right panel
3. Click **Verify** — the audit report appears below the toolbar with the verdict badge
4. Use the **Clear** button to reset for a new document

---

## Troubleshooting

**App starts but translation fails**
Your API key isn't loading. Check `.env` exists in the project root, contains `GROQ_API_KEY=gsk_...`, no spaces around `=`.

**Port 5000 already in use**
```bash
docker run --env-file .env -p 5001:5000 tarjama
# Then open http://localhost:5001
```

**PDF content not appearing**
The PDF may be image-based (scanned). `pdfplumber` can only extract selectable text — it cannot OCR scanned images.

**Docker build fails**
Make sure Docker Desktop is running before building.

---

## Project Structure

```
AI-Translator/
├── app.py              # Flask backend — upload, translate, verify routes
├── index.html          # Frontend — split-screen UI, toolbar, report panel
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image
├── docker-compose.yml  # docker compose up/down
├── .env.example        # Copy to .env and add your key
└── .gitignore
```

---

## Security

<<<<<<< HEAD
- Never share or commit your `.env` file
- The app has no authentication — do not expose it to the public internet without adding auth
=======

Setup and Installation
There are two ways to run this application — using Docker (recommended for reviewers and non-developers) or running it directly with Python.

Option 1 — Docker (Recommended for reviewers)
This is the easiest option. You do not need Python, pip, or any development tools installed. You only need Docker Desktop and a Groq API key.
Step 1 — Install Docker Desktop
Download and install from docker.com. Once installed, make sure it is running before proceeding.
Step 2 — Get a free Groq API key
Go to console.groq.com, sign up for a free account, and generate an API key. No credit card is required.
Step 3 — Clone the repository

git clone https://github.com/uchihamadara69404/AI-Translator.git
cd AI-Translator


Step 4 — Create your environment file
In the project folder, create a file called .env and add the following line:

GROQ_API_KEY=your-groq-api-key-here


Replace your-groq-api-key-here with the key you generated in Step 2. A template file called .env.example is included in the repo for reference.
Step 5 — Run the application

docker-compose up


Step 6 — Open the app
Go to http://localhost:5000 in your browser. The application is ready to use.
To stop the application, press Ctrl+C in the terminal.

Option 2 — Run Locally with Python
Use this option if you have Python installed and prefer not to use Docker.
Step 1 — Get a free Groq API key
Go to console.groq.com, sign up, and generate an API key. No credit card is required.
Step 2 — Clone the repository

git clone https://github.com/uchihamadara69404/AI-Translator.git
cd AI-Translator


Step 3 — Install dependencies

pip install flask pdfplumber groq


Step 4 — Set your API key

export GROQ_API_KEY="your-groq-api-key-here"


Step 5 — Run the application

python app.py


Step 6 — Open the app
Go to http://127.0.0.1:5000 in your browser.

Option 3 — GitHub Codespaces (For developers)
Step 1 — Add your Groq API key as a Codespace secret
Go to GitHub → Settings → Codespaces → Secrets and add GROQ_API_KEY. It will be automatically injected into every Codespace session.
Step 2 — Open the repo in Codespaces and run

pip install flask pdfplumber groq
python app.py


A popup will appear to open the forwarded port directly in your browser.
>>>>>>> ea2499e (Update: ReadME file)
