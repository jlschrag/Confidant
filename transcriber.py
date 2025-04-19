import os
import time
import whisperx

from typing import List
from datetime import datetime
from wakeonlan import send_magic_packet

from config import TranscriptionSetConfig
from file_system_utils import FileSystemUtils


class Transcriber():
    def __init__(self, model):
        self.model = model

    def _transcribe_audio(self, file_path: str) -> str:
        """Transcribes audio using whisperx and returns the text."""
        audio = whisperx.load_audio(file_path)
        result = self.model.transcribe(audio)        
        return "\n\n".join(segment["text"] for segment in result["segments"])

    def _get_output_filename(self, file_path: str) -> str:
        """
        Generates an output filename based on the file name or creation date.
        Prefer the filename because creation date could change when file is copied.
        """
        filename, _ = os.path.splitext(os.path.basename(file_path))
        
        if "my recording" in filename.lower() or "new recording" in filename.lower():
            creation_time = os.path.getctime(file_path)
            filename = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d_%H-%M-%S")
            
        return filename + ".txt"
    
    def _write_file(self, path: str, filename: str, contents: str, retry_count: int, retry_delay: int) -> bool:
        output_path = os.path.join(path, filename)
        
        for attempt in range(retry_count):
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(contents)
                print(f"Processed {filename} to {path}")
                return True
            except:
                self._send_wake_on_lan()
                    
                time.sleep(retry_delay)
                print(f"Retrying write of {filename} to {path}")
                
        return False
    
    def _send_wake_on_lan(self):
        mac_address = "00:11:32:71:DE:12"
        
        try:
            send_magic_packet(mac_address, ip_address="192.168.1.255") #################################### Replace
        except Exception as ex:
            print(ex)

    def process_files(self, transcription_sets: List[TranscriptionSetConfig]) -> None:
        """Processes audio files based on transcription configurations."""
        for ts in transcription_sets:
            for input_dir in ts.audio_inputs:
                for output in ts.text_outputs:
                    os.makedirs(output.directory, exist_ok=True)
                
                for file_name in FileSystemUtils.list_files_by_mtime(input_dir):
                    file_path = os.path.join(input_dir, file_name)
                    output_filename = self._get_output_filename(file_path)
                    deadletter_filepath = os.path.join(ts.deadletter_output.directory, output_filename)
                    
                    if os.path.getsize(file_path) > 10 * 1024 * 1024:  # MB in bytes
                        print(f"Skipping {output_filename}. > max size")
                        continue
                    
                    if os.path.exists(deadletter_filepath):
                        continue
                    
                    # TODO: There is a bug here. If multiple outputs are configured, based on filter keywords, and one previously succeeded while the others failed,
                    # This will skip reprocessing.
                    file_already_processed = False
                    for output in ts.text_outputs:
                        output_path = os.path.join(output.directory, output_filename)
                        if os.path.exists(output_path):
                            print(f"Skipping {file_path}. File already exists in {output.directory}.")
                            file_already_processed = True
                            break;
                        
                    if file_already_processed:
                        continue
                    
                    print(f"Processing {file_path}")
                                            
                    transcription: str = self._transcribe_audio(file_path)
                    first_12_words: List[str] = transcription.lower().split()[:12]
                    
                    processed = False
                            
                    for output in ts.text_outputs:
                        if not output.keyword or output.keyword in first_12_words:
                            processed = self._write_file(output.directory, output_filename, transcription, output.retry_count, output.retry_delay)
                    
                    if not processed:
                        os.makedirs(ts.deadletter_output.directory, exist_ok=True)
                        self._write_file(ts.deadletter_output.directory, 
                                         output_filename, 
                                         transcription, 
                                         ts.deadletter_output.retry_count, 
                                         ts.deadletter_output.retry_delay)