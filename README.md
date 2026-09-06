# Meeting Notes to PDF

A local, AI-powered app that turns messy meeting notes into well-organized PDF documents — **no cloud, all processing happens on your machine** using Ollama's local models.

## Features

- Paste raw meeting notes or load from a `.txt` file
- Local AI (Ollama) restructures notes into clean sections: Summary, Key Discussion Points, Decisions, Action Items, Next Steps
- Generates a professional, styled PDF
- Runs 100% locally — your notes never leave your machine
- Two interfaces: a desktop GUI (Tkinter) and a modern web UI (Flask + HTML/CSS/JS)

## Requirements

- **Python 3.9+**
- **Ollama** — [Download here](https://ollama.com/download)

## Setup

1. Install dependencies (and check Ollama):
   ```
   setup.bat
   ```
   Or manually:
   ```
   pip install fpdf2 requests ollama flask
   ```

2. Install a local AI model (one-time):
   ```
   ollama pull llama3.1
   ```

## Run

Desktop GUI:
```
python app.py
```

Web UI:
```
python web_app.py
```
Then open http://127.0.0.1:5000 in your browser.

## Usage

1. Start Ollama (the app, or run `ollama serve`). If Ollama isn't running, just launch it — it auto-starts in the background on most installs.
2. Launch the app: `python app.py` (desktop) or `python web_app.py` (web UI → http://127.0.0.1:5000).
3. Paste your meeting notes (or browse to a `.txt` file).
4. Select/confirm a model.
5. Click **Generate PDF** and choose where to save.

## Project Structure

```
app.py                  # Tkinter desktop GUI
web_app.py              # Flask web server (reuses the modules below)
templates/
  index.html            # Web UI (HTML + CSS + JS, no build step)
modules/
  ai_processor.py       # Ollama integration (prompts + JSON parsing)
  pdf_generator.py      # PDF layout & generation (fpdf2)
```

## Suggested Models

| Model | Command |
|-------|---------|
| llama3.1 (recommended) | `ollama pull llama3.1` |
| llama3.2 | `ollama pull llama3.2` |
| mistral | `ollama pull mistral` |
| gemma2 | `ollama pull gemma2` |

## Project Structure

```
app.py                  # Tkinter desktop GUI
web_app.py              # Flask web server (reuses the modules below)
templates/
  index.html            # Web UI (HTML + CSS + JS, no build step)
modules/
  ai_processor.py       # Ollama integration (prompts + JSON parsing)
  pdf_generator.py      # PDF layout & generation (fpdf2)
```

## Troubleshooting

- **"No models found"** → Ollama isn't running or has no models. Run `ollama pull llama3.1` and `ollama list`.
- **Tkinter errors** → Install Python with Tk: `pip install tk` (or reinstall Python with Tcl/Tk enabled).
- **Web UI won't start** → Make sure Flask is installed: `pip install flask`. The web server logs to `logs/web_app.log`.
