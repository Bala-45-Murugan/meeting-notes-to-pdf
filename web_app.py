import io
import logging
import sys
import os
import threading
from datetime import datetime

from flask import Flask, jsonify, render_template, request, send_file

from modules.ai_processor import process_notes, get_installed_models
from modules.pdf_generator import generate_pdf

app = Flask(__name__)

logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "web_app.log"),
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    encoding="utf-8",
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/models")
def models():
    installed = get_installed_models()
    fallback = ["llama3.1", "llama3.2", "llama3.3", "mistral", "gemma2", "qwen2.5"]
    return jsonify({"models": installed or fallback, "installed": bool(installed)})


@app.route("/api/generate", methods=["POST"])
def generate():
    body = request.get_json(silent=True) or {}
    notes = (body.get("notes") or "").strip()
    model = body.get("model") or "llama3.1"

    if not notes:
        return jsonify({"error": "No notes provided."}), 400

    try:
        data = process_notes(notes, model=model)

        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        tmp_pdf = os.path.join(
            log_dir, f"meeting_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        generate_pdf(data, tmp_pdf)

        return send_file(
            tmp_pdf,
            as_attachment=True,
            download_name="meeting_notes.pdf",
            mimetype="application/pdf",
        )
    except Exception as e:
        app.logger.exception("PDF generation failed")
        return jsonify({"error": str(e)}), 500


def _run():
    port = int(os.environ.get("PORT", 5000))
    print(f"\n  Meeting Notes to PDF web UI:  http://127.0.0.1:{port}\n")
    app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    _run()
