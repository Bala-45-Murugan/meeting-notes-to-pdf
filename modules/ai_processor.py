import json
import logging
import re
import ollama

logger = logging.getLogger(__name__)


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
    logger.warning("Raw model response >>> %r", content)

    return parse_json_response(content)


def parse_json_response(content: str) -> dict:
    """Parse the model's text response into a dict, tolerating fenced code
    blocks, leading/trailing noise, and extra prose around the JSON object."""
    cleaned = content.strip()

    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        cleaned = cleaned[first_brace : last_brace + 1]

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        logger.warning("Strict JSON parse failed. Attempting repair: %r", cleaned)
        repaired = repair_json(cleaned)
        return json.loads(repaired)


def repair_json(text: str) -> str:
    """Best-effort repairs for common model JSON mangling: trailing commas,
    single quotes, unquoted keys, and stray backslashes."""
    result = []
    i = 0
    n = len(text)
    in_string = False
    while i < n:
        ch = text[i]
        if ch == '"' and not in_string:
            in_string = True
            result.append(ch)
        elif ch == '"' and in_string:
            in_string = False
            result.append(ch)
        elif ch == "'" and not in_string:
            result.append('"')
        elif in_string and ch == "\\" and i + 1 < n and text[i + 1] == "'":
            result.append("'")
            i += 1
        else:
            result.append(ch)
        i += 1

    rebuilt = "".join(result)
    rebuilt = re.sub(r",(\s*[}\]])", r"\1", rebuilt)
    rebuilt = re.sub(r"([{,])\s*([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', rebuilt)
    rebuilt = rebuilt.replace("\\'", "'")
    return rebuilt
