import os

class FileSystemUtils:
    @staticmethod
    def list_files_by_mtime(directory: str):
        """Returns a list of files sorted by modified date (newest first)."""
        with os.scandir(directory) as entries:
            files = [(entry.name, entry.stat().st_mtime) for entry in entries if entry.is_file() and entry.name.endswith(('.mp3', '.wav', '.m4a', '.flac'))]
        
        # Sort files by modified time (newest first)
        files.sort(key=lambda x: x[1], reverse=True)
        
        return [file[0] for file in files]  # Return only filenames
    
    @staticmethod
    def list_text_files_by_name_asc(directory: str):
        with os.scandir(directory) as entries:
            files = [entry.name for entry in entries if entry.is_file() and entry.name.endswith(('.txt'))]
        
        files.sort()
        
        return files