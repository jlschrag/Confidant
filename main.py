import torch
import whisperx

from config import load_config_from
from transcriber import Transcriber
from aggregator import Aggregator
from sorter import Sorter
                            
                            
if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisperx.load_model("large-v2", device, compute_type="float32", language="en")
    
    t = Transcriber(model)
    
    config = load_config_from("config.yaml")
    s = Sorter()
    agg = Aggregator(config.aggregations)
    
    t.process_files(config.transcription_sets)
    
    s.sort()
    
    agg.aggregate_text_files()
