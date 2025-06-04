import json
import os
import datetime


def save_json(data, filepath):
    """Saves a Python object as a pretty JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_text_safe(element):
    """Safely get text content from a selenium element."""
    try:
        return element.text.strip()
    except Exception:
        return ""


def log_error(message):
    """Log error messages with timestamps to logs/errors.log."""
    os.makedirs("logs", exist_ok=True)
    with open("logs/errors.log", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] ERROR: {message}\n")
