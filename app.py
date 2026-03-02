from flask import Flask, request, jsonify, send_from_directory
import pdfplumber
import groq
import os
import io
import json

app = Flask(__name__)
client = groq.Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.3-70b-versatile"

def chat(system, user):
    r = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    return r.choices[0].message.content

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files["pdf"]
        pages = []
        with pdfplumber.open(io.BytesIO(file.read())) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text(layout=True)
                if text:
                    header = f"\n\n--- Page {i + 1} ---\n\n" if i > 0 else ""
                    pages.append(header + text)
        return jsonify({"text": "".join(pages).strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/translate", methods=["POST"])
def translate():
    try:
        text = request.json["text"]
        result = chat(
            "You are an expert English-to-Arabic translator for official and legal documents. "
            "Preserve ALL formatting: paragraph breaks, bullet points, numbering, indentation. "
            "Output only the translated Arabic text, nothing else.",
            f"Translate to Arabic:\n\n{text}"
        )
        return app.response_class(
            response=json.dumps({"translation": result}, ensure_ascii=False),
            mimetype="application/json"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/verify", methods=["POST"])
def verify():
    try:
        original = request.json["original"]
        translation = request.json["translation"]
        result = chat(
            "You are a senior bilingual Arabic-English translation auditor specializing in official and legal documents. Be rigorous and critical.",
            f"""Perform a rigorous word-for-word and context-for-context audit.

ORIGINAL ENGLISH:
{original}

ARABIC TRANSLATION:
{translation}

Provide a structured report covering:
1. Overall Accuracy Score (0-100%)
2. Semantic Accuracy – does the meaning transfer correctly?
3. Contextual Fidelity – are legal/cultural nuances preserved?
4. Terminology Issues – list any mistranslated or ambiguous terms
5. Structural Integrity – is document structure preserved?
6. Critical Errors – flag anything wrong in sensitive/official content
7. Verdict: APPROVED / NEEDS REVISION / REJECTED with reasoning"""
        )
        return app.response_class(
            response=json.dumps({"report": result}, ensure_ascii=False),
            mimetype="application/json"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
