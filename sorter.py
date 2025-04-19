import os
import shutil
from pathlib import Path

class Sorter:
    def _contains_standup_phrase(self, text: str) -> bool:
        """Checks if any variation of 'standup' appears in the first 12 words."""
        words = text.lower().split()
        first_12 = words[:12]
        joined = " ".join(first_12)
        return any(phrase in joined for phrase in ["stand", "stand-up", "standup"])

    def sort(self) -> None:
        input_path = Path("/mnt/documents/Transcription/Unsorted")
        output_path = Path("/mnt/documents/Transcription/Standup")
        # output_path.mkdir(parents=True, exist_ok=True)

        for file in input_path.glob("*.txt"):
            try:
                with file.open("r", encoding="utf-8") as f:
                    content = f.read()
                    if self._contains_standup_phrase(content):
                        shutil.move(str(file), output_path / file.name)
                        print(f"Moved: {file.name}")
            except Exception as e:
                print(f"Error processing {file.name}: {e}")