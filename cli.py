import argparse
from transcribe import transcribe_audio

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files using WhisperX")
    parser.add_argument("input_dir", help="Path to directory containing audio files")
    parser.add_argument("output_dir", help="Path to save transcriptions")
    # args = parser.parse_args()
    
    working_dir = "/mnt/documents/Transcription"
    input_dir = f"{working_dir}/standup"
    output_dir = f"{working_dir}/transcription"

    transcribe_audio(input_dir, output_dir) # args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()
