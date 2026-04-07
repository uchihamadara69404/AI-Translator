Here’s the full README content — copy and paste this directly into your README.md:

Tarjama · ترجمة
Official Document Translation Suite — English to Arabic

Overview
Tarjama is an AI-powered web application designed to translate official English PDF documents into Arabic with full formatting preservation. It was built specifically for use cases involving sensitive, legal, or governmental content where translation accuracy is non-negotiable.
The application does not simply translate text — it runs a second independent AI verification pass that audits the translation word-for-word and context-for-context, returning a structured accuracy report and a final verdict of APPROVED, NEEDS REVISION, or REJECTED. This dual-layer approach ensures that nuance, terminology, and document structure are not lost in translation.

Problem Statement
Standard translation tools treat documents as raw strings of text. They strip formatting, ignore document hierarchy, and provide no mechanism for validating the output. For official use — legal filings, government documents, HR records, medical reports — this is unacceptable. A mistranslated term or a lost paragraph break can have serious real-world consequences.
Tarjama was built to solve this by combining format-preserving PDF extraction, a translation model with explicit structural instructions, and a fully independent verification layer that flags errors before the output is accepted.

Features
Format-Preserving Extraction
The PDF is parsed using pdfplumber, which reconstructs the document layout by grouping text items according to their vertical and horizontal positions on the page. Paragraphs, bullet points, numbered lists, indentation, and multi-column structures are preserved as faithfully as possible.
AI Translation
The extracted text is sent to Groq’s llama-3.3-70b-versatile model with a system prompt that explicitly instructs it to act as an expert translator for official documents and to output only the Arabic translation with all formatting intact. No preamble, no explanation — just the translated document.
Independent Dual-Layer Verification
A second, completely separate API call is made using a different system prompt that frames the model as a senior bilingual Arabic-English auditor. This call receives both the original English and the translated Arabic and produces a structured audit report. The separation is intentional — having the same model validate its own output in a single call introduces self-validation bias. Two independent calls with opposing personas produce a more objective result.
Structured Audit Report
The verification report covers the following:
	∙	Overall Accuracy Score (0–100%)
	∙	Semantic Accuracy — whether the meaning transfers correctly
	∙	Contextual Fidelity — whether cultural and legal nuance is preserved
	∙	Terminology Issues — any mistranslated or ambiguous terms
	∙	Structural Integrity — whether the document layout survived translation
	∙	Critical Errors — anything specifically wrong in sensitive content
	∙	Final Verdict — APPROVED, NEEDS REVISION, or REJECTED with reasoning
Split-Screen Interface
The original English document is displayed on the left panel. The Arabic translation is displayed on the right panel in proper right-to-left (RTL) formatting with Arabic typography. Both panels scroll independently.
Verification Badge
The final verdict appears as a color-coded badge in the toolbar — green for APPROVED, amber for NEEDS REVISION, red for REJECTED. The full report is accessible via a collapsible panel beneath the toolbar.
Clear Functionality
A Clear button resets both panels, removes the verification report, and returns the interface to its initial state, ready for a new document.

Tech Stack
The backend is built with Python and Flask, which handles three routes: PDF upload and extraction, translation, and verification. PDF parsing is done using pdfplumber with layout mode enabled, which reconstructs document structure from the raw positional data of each text item on the page. The AI model powering both translation and verification is Groq’s llama-3.3-70b-versatile, accessed via the Groq API. Groq runs on custom Language Processing Units (LPUs) rather than GPUs, which makes inference significantly faster than comparable providers. The frontend is built in plain HTML, CSS, and vanilla JavaScript with no frameworks or dependencies. The project is version-controlled on GitHub and was developed inside GitHub Codespaces.

Architecture

User Browser
     │
     ▼
index.html (Frontend)
     │
     ├── POST /upload  ──► pdfplumber extracts + preserves layout
     │                          │
     │                          ▼
     │                    Returns plain text to frontend
     │
     ├── POST /translate ──► Groq API (Translator persona)
     │                          │
     │                          ▼
     │                    Returns Arabic translation
     │
     └── POST /verify  ──► Groq API (Auditor persona)
                                │
                                ▼
                          Returns structured audit report


Project Structure

AI-Translator/
├── app.py          # Flask backend — all three API routes
├── index.html      # Frontend — split-screen UI, toolbar, report panel
├── translator.py   # Standalone CLI version of the pipeline
└── README.md


Here’s the updated README section — replace everything from Setup and Installation onwards in your current README with this:


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
