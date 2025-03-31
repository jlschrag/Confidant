1. Create a `config.yaml` in the root directory with the following structure:
```yaml
- transcription-set:
    audio-inputs:
      - directory: /mnt/unsorted_recordings
      - directory: /Misc
    text-outputs:
      - directory: /mnt/tasks
        filter:
          keyword: task
      - directory: /mnt/journal
        filter:
          keyword: journal
    audio-inputs:
      - directory: /mnt/presorted/tasks
    text-outputs:
      - directory: /mnt/tasks
```
2. `uv run python main.py`
