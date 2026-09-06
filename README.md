# Meeting Notes to PDF

A local, AI-powered app that turns messy meeting notes into well-organized PDF documents — **no cloud, all processing happens on your machine** using Ollama's local models.

## Features

- Paste raw meeting notes or load from a `.txt` file
- Local AI (Ollama) restructures notes into clean sections: Summary, Key Discussion Points, Decisions, Action Items, Next Steps
- Generates a professional, styled PDF
- Runs 100% locally — your notes never leave your machine

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
   pip install fpdf2 requests ollama
   ```

2. Install a local AI model (one-time):
   ```
   ollama pull llama3.1
   ```

## Run

```
python app.py
```

## Usage

1. Start Ollama (the app, or run `ollama serve`). If Ollama isn't running, just launch it — it auto-starts in the background on most installs.
2. Launch the app with `python app.py`.
3. Paste your meeting notes (or browse to a `.txt` file).
4. Select/confirm a model.
5. Click **Generate PDF** and choose where to save.

## Suggested Models

| Model | Command |
|-------|---------|
| llama3.1 (recommended) | `ollama pull llama3.1` |
| llama3.2 | `ollama pull llama3.2` |
| mistral | `ollama pull mistral` |
| gemma2 | `ollama pull gemma2` |

## Project Structure

```
app.py                  # Tkinter GUI
modules/
  ai_processor.py       # Ollama integration (prompts + JSON parsing)
  pdf_generator.py      # PDF layout & generation (fpdf2)
```

## Troubleshooting

- **"No models found"** → Ollama isn't running or has no models. Run `ollama pull llama3.1` and `ollama list`.
- **Tkinter errors** → Install Python with Tk: `pip install tk` (or reinstall Python with Tcl/Tk enabled).
