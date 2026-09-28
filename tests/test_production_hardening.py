from fastapi.testclient import TestClient

from app.core.exceptions import AppException
from app.main import app


client = TestClient(app)


def test_root_endpoint_is_healthy():
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "running"
    assert payload["environment"] == "production"


def test_custom_app_exception_has_consistent_payload():
    @app.get("/raise-app-error")
    def raise_app_error():
        raise AppException("custom problem", status_code=418, code="custom_problem")

    response = client.get("/raise-app-error")
    assert response.status_code == 418
    assert response.json()["detail"] == "custom problem"
    assert response.json()["code"] == "custom_problem"
