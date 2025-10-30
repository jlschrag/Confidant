# Pasted from ChatGPT.  No testing.

import os
import subprocess

NOTES_DIR = "notes"
merged_notes = []

for filename in os.listdir(NOTES_DIR):
    if filename.endswith(".txt") or filename.endswith(".md"):
        with open(os.path.join(NOTES_DIR, filename), "r", encoding="utf-8") as f:
            content = f.read()
            merged_notes.append(f"# {filename}\n{content}")

full_input = "\n\n".join(merged_notes)

# Example prompt to find parallels
prompt = f"""You are an AI assistant. Read the following collection of personal notes. 
Identify patterns, recurring themes, or philosophical parallels between different parts. 
Highlight any surprising or interesting connections. Output a summary of key relationships.

Notes:
{full_input}
"""

# Send to a local LLM (example using ollama)
subprocess.run(["ollama", "run", "llama3:8b-instruct"], input=prompt.encode())
