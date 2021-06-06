import os
from config import FOLDER_STRUCTURE


def create_folder_structure() -> None:
    for _, folder_path in FOLDER_STRUCTURE.items():
        try:
            os.mkdir(folder_path)
        except FileExistsError:
            pass
    return None