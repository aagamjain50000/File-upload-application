import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_file():
    with open("test_file.csv", "wb") as f:
        f.write(b"col1,col2\nval1,val2\n")

    response = client.post("/upload", files={"files": ("test_file.csv", open("test_file.csv", "rb"))})
    assert response.status_code == 200
    assert "test_file.csv" in response.json()

def test_list_files():
    response = client.get("/files")
    assert response.status_code == 200
    assert len(response.json()) > 0  # Assuming there are uploaded files
