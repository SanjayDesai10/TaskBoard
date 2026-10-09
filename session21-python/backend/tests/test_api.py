import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine

# Ensure test database tables are created
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_health():
    assert client.get("/health").json() == {"status": "UP"}

def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "READY"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "TaskBoard API"

def test_create_task_validation():
    response = client.post(
        "/api/tasks",
        json={"title": "Deploy application", "priority": "HIGH", "assignee": "Student"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Deploy application"
    assert data["priority"] == "HIGH"
    assert data["status"] == "TODO"

def test_list_tasks():
    response = client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) >= 1

def test_get_stats():
    response = client.get("/api/tasks/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "total" in stats
    assert stats["total"] >= 1
