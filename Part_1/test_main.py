from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Hello welcome to the Assignment_4"}


def test_getdata():
    response = client.get("/v1/access?url=s3%3A%2F%2Fner-api2-team6%2Finputpii%2FAGEN.txt")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_ananomize():
    response = client.get("v1/maskedandanonymized?s3_path=s3%3A%2F%2Frishvita%2Fsec-edgar%2Ftranscripts%2FAGEN.txt&Mask_Entity=NAME&deidentify_Ent=DATE")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_nerdata():
    response = client.get("/v1/ner?url=s3%3A%2F%2Fner-api2-team6%2Finputpii%2FAGEN.txt")
    assert response.status_code == 200
    assert len(response.json()) > 0