# Agent Instructions

This is a Python Tkinter desktop app that converts meeting notes to PDF using local AI (Ollama, http://localhost:11434).

## Critical rules
- Never call self.root.after() or update Tkinter widgets directly from a background thread - Tkinter is not thread-safe.
- Use queue.Queue for communication between background threads and the main thread; poll the queue every ~100ms on the main thread.
- Any error from a background task must be surfaced to the user via a message box, not fail silently.

## Structure
- app.py - main GUI entry point
- modules/ai_processor.py - handles Ollama calls
- modules/pdf_generator.py - handles PDF generation
- test_pdf.py - manual test script

## Testing
After any change to app.py or modules/, run python app.py, paste sample notes, and confirm Generate PDF produces a valid PDF with no thread errors.
