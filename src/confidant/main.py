from confidant.aggregator import Aggregator
from confidant.config import load_config_from
from confidant.converter import Converter
from confidant.sorter import Sorter
from confidant.transcriber import Transcriber


if __name__ == "__main__":
    t = Transcriber()

    config = load_config_from("config.yaml")
    s = Sorter()
    agg = Aggregator(config.aggregations)
    
    t.process_files(config.transcription_sets)
    s.sort()
    agg.aggregate_text_files()
    
    Converter.run_conversions(config)
