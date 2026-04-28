# tools.py
from pathlib import Path    
import os

def read_file(path: str):
    return Path(path).read_text()


def write_file(path: str, content: str):
    Path(path).write_text(content)
    return "file updated"

def list_files(path='.'):
    return "\n".join(os.listdir(path))


