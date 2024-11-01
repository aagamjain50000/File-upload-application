import os

CHUNK_SIZE = 1024 * 1024  # 1MB

def save_file_chunk(file_path: str, chunk: bytes):
    with open(file_path, "ab") as f:
        f.write(chunk)

def is_file_complete(file_path: str, total_size: int) -> bool:
    if os.path.exists(file_path):
        return os.path.getsize(file_path) == total_size
    return False
