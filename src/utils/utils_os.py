# Import necessary libraries
import os

def check_directory(path):
    """Create a directory if it does not exist."""
    if not os.path.exists(path):
            os.makedirs(path)


def remove_files(path):
    """Remove files from a folder."""
    files = os.listdir(path)
    if len(files) > 0:
        for f in files:
            os.remove(path / f)