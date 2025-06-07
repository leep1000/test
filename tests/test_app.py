import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import os
import tempfile
import pytest
from app import create_app, db
from app.models import User, Asset

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path,
                      'TESTING': True})
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # create admin user
            admin = User(username='admin', role='admin')
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
        yield client
    os.close(db_fd)
    os.unlink(db_path)


def register(client, username, password, role='regular'):
    return client.post('/register', data={'username': username, 'password': password, 'role': role}, follow_redirects=True)


def login(client, username, password):
    return client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)


def test_register_login(client):
    rv = register(client, 'user1', 'pass')
    assert b'Registration successful' in rv.data
    rv = login(client, 'user1', 'pass')
    assert b'Logged in successfully' in rv.data


def test_asset_crud(client):
    register(client, 'user1', 'pass')
    login(client, 'user1', 'pass')
    rv = client.post('/asset/create', data={'name': 'Laptop', 'asset_type': 'PC', 'serial_number': 'SN123', 'location': 'Office'}, follow_redirects=True)
    assert b'Asset created' in rv.data
    asset = Asset.query.first()
    rv = client.post(f'/asset/{asset.id}/edit', data={'name': 'Laptop2', 'asset_type': 'PC', 'serial_number': 'SN123', 'location': 'Office'}, follow_redirects=True)
    assert b'Asset updated' in rv.data

    # regular user cannot delete
    rv = client.post(f'/asset/{asset.id}/delete', follow_redirects=True)
    assert b'Only admin can delete assets' in rv.data

    # login as admin
    login(client, 'admin', 'admin')
    rv = client.post(f'/asset/{asset.id}/delete', follow_redirects=True)
    assert b'Asset deleted' in rv.data
