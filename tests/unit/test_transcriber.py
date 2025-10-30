from confidant.transcriber import Transcriber
from datetime import datetime


def test_get_output_filename_with_normal_name():
    filename = Transcriber._get_output_filename("/path/to/a/normal_filename.mp3")
    assert filename == "normal_filename.txt"


def test_get_output_filename_with_new_recording(monkeypatch):
    monkeypatch.setattr(
        "os.path.getctime", lambda _: datetime(2023, 10, 26, 10, 30, 0).timestamp()
    )
    filename = Transcriber._get_output_filename("/path/to/a/New Recording 2.m4a")
    assert filename == "2023-10-26_10-30-00.txt"
