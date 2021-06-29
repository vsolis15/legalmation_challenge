from app import app
import pytest

@pytest.fixture
def client():
    # Create a test client using the Flask application configured for testing
    with app.test_client() as client:
        # Establish an application context
        with app.app_context():
            yield client  # this is where the testing happens


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

    response= client.post('/')
    assert response.status_code == 302

def test_api(client):
    response = client.get('/api/files')
    assert response.status_code == 200
    
    assert len(response.get_json()) == 3

    response = client.get('/api/get_file/1')
    assert response.status_code == 200
    assert len(response.get_json()) == 4

