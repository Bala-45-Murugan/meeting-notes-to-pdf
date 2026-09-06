import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import queue
import os
import sys
import logging
from datetime import datetime
from modules.ai_processor import get_installed_models, process_notes, AVAILABLE_MODELS
from modules.pdf_generator import generate_pdf


def _setup_logging():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(
        log_dir, f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        encoding="utf-8",
    )
    logging.getLogger().info("App started. Log file: %s", log_file)
    return log_file


class MeetingNotesApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Meeting Notes to PDF")
        self.root.geometry("900x700")
        self.root.minsize(700, 500)
        self.root.configure(bg="#f0f2f5")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), background="#f0f2f5", foreground="#1a1a2e")
        self.style.configure("Sub.TLabel", font=("Segoe UI", 10), background="#f0f2f5", foreground="#555")
        self.style.configure("Action.TButton", font=("Segoe UI", 11, "bold"), padding=(20, 10))
        self.style.configure("Model.TCombobox", font=("Segoe UI", 10))

        self._build_ui()
        self._load_models()
        self.root.after(100, self._poll_queue)

    def _build_ui(self):
        self.result_queue = queue.Queue()
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main, text="Meeting Notes to PDF", style="Title.TLabel").pack(anchor="w")
        ttk.Label(main, text="Paste your notes below. AI will organize them into a structured PDF.", style="Sub.TLabel").pack(anchor="w", pady=(0, 10))

        ctrl_frame = ttk.Frame(main)
        ctrl_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(ctrl_frame, text="Model:", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        self.model_var = tk.StringVar()
        self.model_combo = ttk.Combobox(ctrl_frame, textvariable=self.model_var, state="readonly", width=30, style="Model.TCombobox")
        self.model_combo.pack(side=tk.LEFT, padx=(5, 15))

        ttk.Button(ctrl_frame, text="Refresh Models", command=self._load_models).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(ctrl_frame, text="Or load from file:", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Button(ctrl_frame, text="Browse...", command=self._load_file).pack(side=tk.LEFT)

        self.notes_text = scrolledtext.ScrolledText(main, wrap=tk.WORD, font=("Consolas", 11), height=20, bg="white", relief=tk.FLAT, borderwidth=2)
        self.notes_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        self.notes_text.insert("1.0", "Paste your meeting notes here...")

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X)

        self.process_btn = ttk.Button(btn_frame, text="Generate PDF", style="Action.TButton", command=self._on_generate)
        self.process_btn.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(btn_frame, mode="indeterminate", length=200)
        self.progress.pack(side=tk.LEFT, padx=(15, 0))

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(btn_frame, textvariable=self.status_var, font=("Segoe UI", 9), foreground="#666").pack(side=tk.LEFT, padx=(15, 0))

    def _load_models(self):
        installed = get_installed_models()
        if installed:
            self.model_combo["values"] = installed
            self.model_combo.current(0)
            self.status_var.set(f"Found {len(installed)} model(s)")
        else:
            self.model_combo["values"] = AVAILABLE_MODELS
            self.model_combo.current(0)
            self.status_var.set("No models found. Install one with: ollama pull llama3.1")

    def _load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.notes_text.delete("1.0", tk.END)
            self.notes_text.insert("1.0", content)

    def _on_generate(self):
        notes = self.notes_text.get("1.0", tk.END).strip()
        if not notes or notes == "Paste your meeting notes here...":
            messagebox.showwarning("No Notes", "Please paste your meeting notes first.")
            return

        model = self.model_var.get()
        if not model:
            messagebox.showwarning("No Model", "Please select or install an AI model.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile="meeting_notes.pdf",
        )
        if not output_path:
            return

        self.process_btn.state(["disabled"])
        self.progress.start(10)
        self.status_var.set("AI is processing your notes... (this can take a minute on local models)")

        thread = threading.Thread(target=self._generate, args=(notes, model, output_path), daemon=True)
        thread.start()

    def _generate(self, notes: str, model: str, output_path: str):
        try:
            data = process_notes(notes, model=model)
            generate_pdf(data, output_path)
            self.result_queue.put(("done", output_path))
        except Exception as e:
            logging.getLogger("app").exception("PDF generation failed")
            self.result_queue.put(("error", str(e)))

    def _poll_queue(self):
        try:
            while True:
                kind, payload = self.result_queue.get_nowait()
                if kind == "done":
                    self._on_done(payload, None)
                else:
                    self._on_done(None, payload)
        except queue.Empty:
            pass
        self.root.after(100, self._poll_queue)

    def _on_done(self, output_path, error):
        self.progress.stop()
        self.process_btn.state(["!disabled"])

        if error:
            self.status_var.set("Error occurred")
            messagebox.showerror("Error", f"Failed to generate PDF:\n\n{error}")
        else:
            self.status_var.set(f"Saved to {os.path.basename(output_path)}")
            messagebox.showinfo("Done", f"PDF saved to:\n{output_path}")


if __name__ == "__main__":
    log_file = _setup_logging()
    root = tk.Tk()
    app = MeetingNotesApp(root)
    root.mainloop()
