import pytest
import yaml
import tempfile
import os
from typing import List
from config import load_config_from, OutputConfig, AggregationConfig  # Replace 'your_module' with the actual module name

def test_load_yaml():
    config = load_config_from("config.yaml")
    ts = config.transcription_sets
    
    assert len(ts) == 5
    assert len(ts[0].audio_inputs) == 5
    assert len(ts[0].text_outputs) == 3
    
    assert isinstance(ts[0].text_outputs[1], OutputConfig)
    assert ts[0].text_outputs[1].directory == "/mnt/documents/Transcription/Journal"
    assert ts[0].text_outputs[1].keyword == "journal"
    
    aggs = config.aggregations
    assert len(aggs) == 1
    assert isinstance(aggs[0], AggregationConfig)
    assert aggs[0].input_directory == "/mnt/documents/Transcription/Standup"
    assert aggs[0].output_filepath == "/mnt/documents/Transcription/StandupAggregation.txt"