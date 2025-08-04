from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient


sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.api.v1.endpoints.health import router


app = FastAPI()
app.include_router(router)


client = TestClient(app)


def test_health_endpoint_returns_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200

