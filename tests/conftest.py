import pytest

from app import create_app
from app.cli import seed_demo
from app.config import TestConfig
from app.extensions import db


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        seed_demo()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, email="admin@studentspot.example.com", password="StudentSpot123!"):
    return client.post(
        "/auth/login",
        data={"login": email, "password": password},
        follow_redirects=True,
    )
