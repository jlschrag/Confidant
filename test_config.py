import pytest
import yaml
import tempfile
import os
from typing import List
from config import load_config_from, TranscriptionSetConfig, OutputConfig  # Replace 'your_module' with the actual module name

def test_load_yaml():
    transaction_sets = load_config_from("config.yaml")

    assert len(transaction_sets) == 5
    assert len(transaction_sets[0].audio_inputs) == 5
    assert len(transaction_sets[0].text_outputs) == 3
    
    assert isinstance(transaction_sets[0].text_outputs[1], OutputConfig)
    assert transaction_sets[0].text_outputs[1].directory == "/mnt/documents/Transcription/Journal"
    assert transaction_sets[0].text_outputs[1].keyword == "journal"
