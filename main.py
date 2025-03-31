import torch
import whisperx

from config import load_config_from
from transcriber import Transcriber

                            
                            
if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisperx.load_model("large-v2", device, compute_type="float32", language="en")
    
    t = Transcriber(model)
    
    config = load_config_from("config.yaml")
    t.process_files(config)
