import os

def calculate_progress(file_path: str, total_size: int) -> int:
    if os.path.exists(file_path):
        uploaded_size = os.path.getsize(file_path)
        return int((uploaded_size / total_size) * 100)
    return 0
