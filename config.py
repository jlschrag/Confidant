import yaml


DEFAULT_RETRY_COUNT = 5
DEFAULT_RETRY_DELAY = 5 # Seconds

class OutputConfig:
    def __init__(self, directory: str, retry_count: int = DEFAULT_RETRY_COUNT, retry_delay: int = DEFAULT_RETRY_DELAY, keyword: str = ""):
        self.directory: str = directory
        self.keyword: str = keyword
        self.retry_count = retry_count
        self.retry_delay = retry_delay

class TranscriptionSetConfig:
    def __init__(self, audio_input: list[dict], outputs: list[OutputConfig], deadletter_output: OutputConfig):
        self.audio_inputs: list[str] = [entry["directory"] for entry in audio_input]
        self.text_outputs: list[OutputConfig] = outputs
        self.deadletter_output: OutputConfig = deadletter_output
        
        
class AggregationConfig:
    def __init__(self, input_directory: str, output_filepath: str, retry_count: int = DEFAULT_RETRY_COUNT, retry_delay: int = DEFAULT_RETRY_DELAY,):
        self.input_directory = input_directory
        self.output_filepath = output_filepath
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        
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
        
        outputs: list[OutputConfig] = []
        for text_output in ts["text-outputs"]:
            keyword = text_output.get("filter", {}).get("keyword", "")
            directory = text_output["directory"]
            retry_count = text_output.get("retry", {}).get("count", DEFAULT_RETRY_COUNT)
            retry_delay = text_output.get("retry", {}).get("delay", DEFAULT_RETRY_DELAY)
            outputs.append(OutputConfig(directory, retry_count, retry_delay, keyword))
        
        deadletter_config = ts.get("deadletter", [])
        deadletter_dir = deadletter_config["text-output"]["directory"] if deadletter_config else ""
        deadletter_output = OutputConfig(deadletter_dir)
        
        transcription_configs.append(TranscriptionSetConfig(ts["audio-inputs"], outputs, deadletter_output))
        
    aggregation_configs: list[AggregationConfig] = []
    for entry in data.get("aggregations", []):
        input_dir = entry["input"]["directory"]
        output_filepath = entry["output"]["filepath"]
        retry_count = entry["output"].get("retry", {}).get("count", DEFAULT_RETRY_COUNT)
        retry_delay = entry["output"].get("retry", {}).get("delay", DEFAULT_RETRY_DELAY)
        aggregation_configs.append(AggregationConfig(input_dir, output_filepath, retry_count, retry_delay))
    
    return Config(transcription_configs, aggregation_configs)