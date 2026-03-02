import pdfplumber
import anthropic
import sys

client = anthropic.Anthropic()


def extract_pdf(path: str) -> str:
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text(layout=True)
            if text:
                header = f"\n\n--- Page {i + 1} ---\n\n" if i > 0 else ""
                pages.append(header + text)
    return "".join(pages).strip()


def translate(text: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        system=(
            "You are an expert English-to-Arabic translator specializing in official, "
            "legal, and governmental documents. Preserve ALL formatting: paragraph breaks, "
            "bullet points, numbering, indentation, and document structure. "
            "Output only the translated Arabic text, nothing else."
        ),
        messages=[{"role": "user", "content": f"Translate the following English text to Arabic:\n\n{text}"}]
    )
    return response.content[0].text


def verify(original: str, translation: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        system=(
            "You are a senior bilingual Arabic-English translation auditor with expertise "
            "in official, legal, and governmental documents. Be rigorous and critical."
        ),
        messages=[{"role": "user", "content": f"""Perform a rigorous word-for-word and context-for-context audit of this translation.

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
7. Verdict: APPROVED / NEEDS REVISION / REJECTED with reasoning"""}]
    )
    return response.content[0].text


def run(pdf_path: str):
    print(f"\n📄 Extracting: {pdf_path}")
    original = extract_pdf(pdf_path)
    print(f"✅ Extracted {len(original.split())} words\n")

    print("─" * 60)
    print("ORIGINAL TEXT (English)")
    print("─" * 60)
    print(original)

    print("\n⏳ Translating to Arabic...")
    arabic = translate(original)
    print("\n" + "─" * 60)
    print("TRANSLATION (Arabic)")
    print("─" * 60)
    print(arabic)

    print("\n⏳ Running verification audit...")
    report = verify(original, arabic)
    print("\n" + "─" * 60)
    print("VERIFICATION REPORT")
    print("─" * 60)
    print(report)

    with open("translation_arabic.txt", "w", encoding="utf-8") as f:
        f.write(arabic)
    with open("verification_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print("\n✅ Saved: translation_arabic.txt & verification_report.txt")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translator.py your_document.pdf")
        sys.exit(1)
    run(sys.argv[1])
