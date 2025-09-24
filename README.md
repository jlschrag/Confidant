Confidant is a voice note transcription app, designed to handle multiple input & output directories, sorting by keyword, note aggregation, & conversion to PDF.  It runs locally, with no data sent to third parties.  It is fully functional - roughly beta state.  But, lets be honest - kinda vibe coded. :)

If `filters` are set for the `text-outputs` in the `config.yaml`, the transcriber will check the first twelve words of a recording for filter keywords and route the resulting transcription files accordingly.

# Setup
1. Clone this repo
2. Create a `config.yaml` in the root directory with the following structure (example - omit any sections not needed):
```yaml
transcription-sets:
  - transcription-set:
      audio-inputs:
        - directory: Recordings/Unsorted
        - directory: Recordings/Unsorted 2021
        - directory: Recordings/Unsorted 2022
        - directory: Recordings/Unsorted 2023
        - directory: Recordings/Misc
      text-outputs:
        - directory: Transcription/Workouts
          filter:
            keyword: workouts
          retry:
            count: 20
            delay: 5
        - directory: Transcription/Workouts
          filter:
            keyword: work
          retry:
            count: 20
            delay: 5
        - directory: Transcription/Workouts
          filter:
            keyword: work-outs
          retry:
            count: 20
            delay: 5
        - directory: Transcription/Journal
          filter:
            keyword: journal
          retry:
            count: 20
            delay: 5
      deadletter:
        text-output:
          directory: Transcription/Unsorted
          retry:
            count: 20
            delay: 5
  - transcription-set:
      audio-inputs:
        - directory: Recordings/Notes
      text-outputs:
        - directory: Transcription/Notes
          retry:
            count: 20
            delay: 5
aggregations:
  - input:
      directory: Transcription/Notes
    output:
      filepath: Transcription/NoteAggregation.txt
      retry:
        count: 20
        delay: 5
pdf_conversions:
  - input:
      directory: "/mnt/documents/Text Files"
    output:
      directory: "/mnt/documents/PDFs"

```
3. `uv run python main.py`
