"""Basic API tests for the health endpoint."""

import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite://"

# Ensure the backend package is importable as ``backend`` and alias it as ``app``.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

import backend as backend_package

sys.modules["app"] = backend_package

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
