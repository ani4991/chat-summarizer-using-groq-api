from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# check for ideal use-case
def test_valid_transcript():
    response = client.post(
        "/summarize",
        json={"transcript": "Agent: Hello, how can I help you?\nCustomer: I have an issue with my order.\nAgent: Sure, let me check that for you.\nCustomer: Thanks!"}
    )
    assert response.status_code == 200
    assert "summary" in response.json()
    assert response.json()["summary"] is not None
    assert response.json()["error"] is None

# check a short input
def test_short_transcript():
    response = client.post(
        "/summarize",
        json={"transcript": "Hi"}
    )
    assert response.status_code == 200
    assert "error" in response.json()
    assert response.json()["error"] == "Transcript is too short or invalid for summarization."

# check the working of model for non_summarization_task
def test_non_summarization_task():
    response = client.post(
        "/summarize",
        json={"transcript": "Can you explain what this conversation means in Spanish?"}
    )
    assert response.status_code == 200
    assert "error" in response.json()
    assert response.json()["error"] == "This endpoint is restricted to transcript summarization tasks only."

# check for junk input - 1 
def test_junk_symbols():
    response = client.post(
        "/summarize",
        json={"transcript": "!@#$%^&*() --- *** ====="}
    )
    assert response.status_code == 200
    assert "error" in response.json()
    assert response.json()["error"] == "Transcript contains too many invalid characters or lacks meaningful content."

# check for junk input - 2
def test_junk_random_letters():
    response = client.post(
        "/summarize",
        json={"transcript": "asdhjkl qwe zxcvbnm pqr"}
    )
    assert response.status_code == 200
    assert "error" in response.json()
    assert response.json()["error"] == "Transcript contains too many invalid characters or lacks meaningful content."

# check for junk input - 3
def test_junk_numbers():
    response = client.post(
        "/summarize",
        json={"transcript": "123456789012345678901234"}
    )
    assert response.status_code == 200
    assert "error" in response.json()
    assert response.json()["error"] == "Transcript contains too many invalid characters or lacks meaningful content."

# check for junk input - 4
def test_junk_mixed():
    response = client.post(
        "/summarize",
        json={"transcript": "!!! ### @@@ xyz"}
    )
    assert response.status_code == 200
    assert "error" in response.json()
    assert response.json()["error"] == "Transcript contains too many invalid characters or lacks meaningful content."
