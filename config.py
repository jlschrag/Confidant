import yaml
from typing import List

class OutputConfig:
    def __init__(self, directory: str, filter: dict | None = None):
        self.directory: str = directory
        self.keyword: str = filter["keyword"] if filter and "keyword" in filter else []

class TranscriptionSetConfig:
    def __init__(self, audio_input: List[dict], outputs: list[OutputConfig]):
        self.audio_inputs: List[str] = [entry["directory"] for entry in audio_input]
        self.text_outputs: List[OutputConfig] = outputs

def load_config_from(yaml_file_path: str) -> List[TranscriptionSetConfig]:
    with open(yaml_file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    
    transcription_configs: List[TranscriptionSetConfig] = []
    for entry in data:
        ts = entry.get("transcription-set", [])
        outputs = [OutputConfig(**output) for output in ts["text-outputs"]]
        transcription_configs.append(TranscriptionSetConfig(ts["audio-inputs"], outputs))
    
    return transcription_configs