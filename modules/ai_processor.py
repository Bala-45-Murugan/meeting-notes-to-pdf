import json
import ollama


SYSTEM_PROMPT = """You are a meeting notes organizer. The user will give you raw meeting notes.
Your job is to restructure them into a clean, professional document with the following sections:

1. **Meeting Title** - A concise descriptive title
2. **Date & Attendees** - If mentioned, extract or infer
3. **Summary** - A 2-4 sentence executive summary
4. **Key Discussion Points** - Bullet points of main topics discussed
5. **Decisions Made** - Clear list of decisions reached
6. **Action Items** - Tasks assigned with owners if mentioned
7. **Next Steps** - Follow-up items or future meeting topics

Rules:
- Output valid JSON with these exact keys: title, date, attendees, summary, discussion_points, decisions, action_items, next_steps
- discussion_points, decisions, action_items, and next_steps are arrays of strings
- attendees is an array of strings (can be empty if not mentioned)
- date is a string (can be empty if not mentioned)
- Be concise but thorough. Preserve all important information from the original notes.
- Do NOT include any text outside the JSON response."""

AVAILABLE_MODELS = [
    "llama3.1",
    "llama3.2",
    "llama3.3",
    "llama3",
    "mistral",
    "mixtral",
    "phi3",
    "gemma2",
    "qwen2.5",
    "deepseek-r1",
]


def get_installed_models() -> list[str]:
    try:
        models = ollama.list()
        return [m.model for m in models.models]
    except Exception:
        return []


def process_notes(raw_notes: str, model: str = "llama3.1") -> dict:
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_notes},
        ],
        options={"temperature": 0.3},
    )

    content = response["message"]["content"].strip()

    if content.startswith("```"):
        lines = content.split("\n")
        lines = lines[1:]  # drop opening ```json
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines)

    return json.loads(content)
