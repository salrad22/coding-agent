# tools.py
from pathlib import Path    
import os

def read_file(path: str):
    return Path(path).read_text()


def write_file(path: str, content: str):
    Path(path).write_text(content)
    return "file updated"

def list_files(path='.'):
    try:
        return "\n".join(os.listdir(path))
    except Exception as e:
        return f"Error listing files: {str(e)}"

