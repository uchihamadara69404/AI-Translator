# AI-Translator
Tarjama · ترجمة
Official Document Translation Suite — English to Arabic
A web-based AI translation tool that converts English PDF documents into Arabic while preserving the original formatting. Built with a dual-layer verification system to ensure translation accuracy for official, legal, and sensitive documents.

Preview
The app features a clean split-screen interface — original English on the left, Arabic translation on the right — with an automated audit report that scores the translation and flags any issues.

Features
	∙	PDF Upload & Extraction — Drag and drop or browse to upload any English PDF. Text is extracted with layout preservation, keeping paragraph structure, bullet points, numbering, and spacing intact.
	∙	AI-Powered Translation — Translates the full document from English to Arabic using Groq’s llama-3.3-70b-versatile model, with explicit instructions to preserve all formatting.
	∙	Dual-Layer Verification — A second independent AI call acts as a senior bilingual auditor, reviewing the translation word-for-word and context-for-context.
	∙	Structured Audit Report — The verification step produces a detailed report covering accuracy score, semantic fidelity, contextual nuance, terminology issues, structural integrity, and a final verdict of APPROVED, NEEDS REVISION, or REJECTED.
	∙	Arabic RTL Rendering — The translated text is displayed right-to-left with proper Arabic typography.

Tech Stack
The backend is built with Python and Flask, handling all routes for PDF processing, translation, and verification. PDF extraction is done using pdfplumber, which preserves layout and formatting better than most alternatives. The AI model powering both translation and verification is Groq’s llama-3.3-70b-versatile, accessed via the Groq API on the free tier. The frontend is plain HTML, CSS, and vanilla JavaScript — no frameworks. The project is developed and hosted on GitHub Codespaces.​​​​​​​​​​​​​​​​

Project Structure
AI-Translator/
├── app.py          # Flask backend — upload, translate, verify routes
├── index.html      # Frontend — split-screen UI
└── README.md


Getting Started
Prerequisites
	∙	Python 3.10+
	∙	A free Groq API key — no credit card required
1. Clone the repository
git clone https://github.com/your-username/AI-Translator.git
cd AI-Translator

2. Install dependencies
pip install flask pdfplumber groq

3. Set your API key
Option A — current session only:
export GROQ_API_KEY="your-key-here"

Option B — persist across sessions:
echo 'export GROQ_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc

Option C — GitHub Codespaces (recommended):
Go to GitHub → Settings → Codespaces → Secrets and add GROQ_API_KEY. It will be automatically injected into every Codespace.

4. Run the app
python app.py
Open your browser at http://127.0.0.1:5000. In Codespaces, a popup will appear to open the forwarded port directly.

How It Works
	1.	Upload — User uploads a PDF. The /upload route extracts text using pdfplumber with layout=True to preserve structure.
	2.	Translate — The /translate route sends the extracted text to Groq with a system prompt instructing it to preserve all formatting and output only Arabic.
	3.	Verify — The /verify route sends both the original and translated text to a second Groq call that acts as an auditor, producing a structured accuracy report.
	4.	Display — The frontend renders both texts side by side. The Arabic panel is RTL. The verification badge and collapsible report appear in the toolbar.

Roadmap
	∙	Download translated Arabic text as .txt or .docx
	∙	Support for multi-language output beyond Arabic
	∙	Chunking support for large PDFs (100+ pages)
	∙	Side-by-side paragraph alignment
	∙	Human review workflow with annotation support

Security Notes
	∙	Never hardcode your API key in the source code
	∙	Always use environment variables or GitHub Secrets
	∙	The .bashrc method exposes the key in your terminal history — prefer GitHub Secrets for Codespaces

Built by Mohammed Kaif Ali