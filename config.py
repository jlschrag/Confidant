import yaml

class OutputConfig:
    def __init__(self, directory: str, filter: dict | None = None):
        self.directory: str = directory
        self.keyword: str = filter["keyword"] if filter and "keyword" in filter else []

class TranscriptionSetConfig:
    def __init__(self, audio_input: list[dict], outputs: list[OutputConfig]):
        self.audio_inputs: list[str] = [entry["directory"] for entry in audio_input]
        self.text_outputs: list[OutputConfig] = outputs
        
class AggregationConfig:
    def __init__(self, input_directory: str, output_filepath: str):
        self.input_directory = input_directory
        self.output_filepath = output_filepath
        
class Config:
    def __init__(self, transcription_sets: list[TranscriptionSetConfig], aggregations: list[AggregationConfig]):
        self.transcription_sets = transcription_sets
        self.aggregations = aggregations
    
def load_config_from(yaml_file_path: str) -> Config:
    with open(yaml_file_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    
    transcription_configs: list[TranscriptionSetConfig] = []
    for entry in data.get("transcription-sets", []):
        ts = entry.get("transcription-set", [])
        outputs = [OutputConfig(**output) for output in ts["text-outputs"]]
        transcription_configs.append(TranscriptionSetConfig(ts["audio-inputs"], outputs))
        
    aggregation_configs: list[AggregationConfig] = []
    for entry in data.get("aggregations", []):
        input_dir = entry["input"]["directory"]
        output_filepath = entry["output"]["filepath"]
        aggregation_configs.append(AggregationConfig(input_dir, output_filepath))
    
    return Config(transcription_configs, aggregation_configs)