import pytest
from fastapi.testclient import TestClient

from voiddrop.config import Config
from voiddrop.security import PinAuth
from voiddrop.server import create_app


def test_pin_auth_constant_time_interface():
    auth = PinAuth("4821")
    assert auth.enabled
    assert auth.verify_pin("4821")
    assert not auth.verify_pin("0000")
    assert not auth.verify_token(None)


def test_pin_gates_sharing_endpoints(tmp_path):
    client = TestClient(create_app(Config(directory=tmp_path, pin="4821")))
    assert client.get("/").status_code == 200
    assert client.get("/api/files").status_code == 401
    assert client.post("/api/login", json={"pin": "no"}).status_code == 401
    assert client.post("/api/login", json={"pin": "4821"}).status_code == 200
    assert client.get("/api/files").status_code == 200


def test_upload_download_delete_and_traversal(tmp_path):
    client = TestClient(create_app(Config(directory=tmp_path)))
    assert client.put("/api/files/hello.txt", content=b"hello").json()["size"] == 5
    assert client.get("/api/files").json()["files"][0]["name"] == "hello.txt"
    assert client.get("/api/files/hello.txt").content == b"hello"
    assert client.put("/api/files/%2E%2E%2Fsecret", content=b"x").status_code in (400, 404)
    assert client.delete("/api/files/hello.txt").json() == {"deleted": True}


def test_upload_collision_does_not_replace_existing(tmp_path):
    (tmp_path / "same.txt").write_text("old")
    client = TestClient(create_app(Config(directory=tmp_path)))
    assert client.put("/api/files/same.txt", content=b"new").status_code == 409
    assert (tmp_path / "same.txt").read_text() == "old"
