from config import load_config_from
from transcriber import Transcriber
from aggregator import Aggregator
from sorter import Sorter
from converter import Converter
                            
                            
if __name__ == "__main__":
    t = Transcriber()

    config = load_config_from("config.yaml")
    s = Sorter()
    agg = Aggregator(config.aggregations)
    
    #t.process_files(config.transcription_sets)
    #s.sort()
    #agg.aggregate_text_files()
    
    Converter.run_conversions(config)
