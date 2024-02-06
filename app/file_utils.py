# file_utils.py

import os

def save_to_file(content, relative_directory, filename):
    """
    Saves the given content to a text file in the specified directory with the given filename.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_directory_path = os.path.join(base_dir, relative_directory)
    if not os.path.exists(full_directory_path):
        os.makedirs(full_directory_path)
    filepath = os.path.join(full_directory_path, filename)
    with open(filepath, 'w') as file:
        file.write(content)
    print(f"Message saved to {filepath}")

def create_directory(directory_name):
    """
    Creates a directory at the specified path relative to the script's location if it doesn't already exist.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_directory_path = os.path.join(base_dir, directory_name)
    os.makedirs(full_directory_path, exist_ok=True)
