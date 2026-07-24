from app import app


def test_home():

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_health():

    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json["status"] == "Application is up and working fine"


def test_version():

    client = app.test_client()

    response = client.get("/version")

    assert response.status_code == 200


def test_metrics():

    client = app.test_client()

    response = client.get("/metrics")

    assert response.status_code == 200
    assert b"# HELP" in response.data
