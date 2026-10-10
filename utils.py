"""Reusable helpers: configuration, Ollama access, formatting and file handling."""

import datetime
import json
import os

import ollama
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

EMAILS_CSV = os.path.join(DATA_DIR, "emails.csv")
REPLY_FILE = os.path.join(OUTPUT_DIR, "generated_reply.txt")
STATE_FILE = os.path.join(OUTPUT_DIR, "session_state.json")

OLLAMA_MODEL = "llama3.2:latest"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

LINE = "=" * 64
DASH = "-" * 64

_client = ollama.Client()


class ModelError(Exception):
    """Raised when the local model cannot serve the request."""


def check_model():
    """Verify the Ollama server is reachable and the model is installed."""
    try:
        models = _client.list()
    except Exception:
        raise ModelError("Cannot reach Ollama. Start it with:  ollama serve")
    names = [m.get("model") or m.get("name") for m in models.get("models", [])]
    if OLLAMA_MODEL not in names:
        raise ModelError("Model {} is not installed. Run:  ollama pull {}".format(
            OLLAMA_MODEL, OLLAMA_MODEL.split(":")[0]))
    return names


def ask(system_prompt, user_prompt, temperature=0.5):
    """Send a prompt to the local model served by Ollama."""
    try:
        response = _client.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_prompt}],
            options={"temperature": temperature},
        )
    except Exception as exc:
        raise ModelError("Model request failed: {}".format(exc))
    text = response["message"]["content"].strip()
    if not text:
        raise ModelError("The model returned an empty response.")
    return text


def banner(title):
    print(LINE)
    print(title)
    print(LINE)


def load_emails():
    """Load the previous customer interactions from the CSV dataset."""
    if not os.path.exists(EMAILS_CSV):
        raise ModelError("Dataset not found at {}".format(EMAILS_CSV))
    return pd.read_csv(EMAILS_CSV)


# ------------------------------------------------------------- session state
def save_state(state):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE) as f:
        return json.load(f)


def update_state(**kwargs):
    state = load_state()
    state.update(kwargs)
    save_state(state)
    return state


def require(key, message):
    """Return a stored value, or None with a message if it is missing."""
    value = load_state().get(key)
    if not value:
        print(message)
    return value


# --------------------------------------------------------------- save reply
def save_reply(state, verbose=True):
    """Q9 - save the email, generated reply, intent and date to a text file."""
    lines = [
        "INTELLIGENT EMAIL ASSISTANT - GENERATED REPLY",
        "=" * 55,
        "Date           : {}".format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M")),
        "Customer Name  : {}".format(state.get("name", "")),
        "Subject        : {}".format(state.get("subject", "")),
        "Detected Intent: {}".format(state.get("intent", "")),
        "=" * 55,
        "",
        "CUSTOMER EMAIL",
        "-" * 55,
        state.get("email", ""),
        "",
        "GENERATED REPLY",
        "-" * 55,
        state.get("reply", ""),
        "",
    ]
    if state.get("summary"):
        lines += ["CONVERSATION SUMMARY", "-" * 55, state["summary"], ""]

    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(REPLY_FILE, "w") as f:
            f.write("\n".join(lines))
    except OSError as exc:
        raise ModelError("Could not save the reply: {}".format(exc))

    if verbose:
        print("Reply saved successfully.")
        print("File       : {}".format(REPLY_FILE))
        print("Intent     : {}".format(state.get("intent", "")))
        print("Characters : {}".format(len("\n".join(lines))))
    return REPLY_FILE
