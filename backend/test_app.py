"""
Unit tests for Flask Backend
Run with: pytest test_app.py -v
"""

import pytest
import json
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Test the home endpoint returns welcome message"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'Jenkins CI/CD Demo' in data['message']


def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data


def test_info_endpoint(client):
    """Test the info endpoint returns app metadata"""
    response = client.get('/api/info')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'name' in data
    assert 'version' in data
    assert 'endpoints' in data


def test_echo_endpoint_with_data(client):
    """Test echo endpoint with JSON data"""
    test_data = {"message": "Hello, Jenkins!", "number": 42}
    response = client.post(
        '/api/echo',
        data=json.dumps(test_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['received'] == test_data
    assert data['message'] == 'Echo successful!'


def test_echo_endpoint_empty(client):
    """Test echo endpoint with no data"""
    response = client.post('/api/echo')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['received'] == {}


def test_pipeline_status_endpoint(client):
    """Test pipeline status endpoint"""
    response = client.get('/api/pipeline-status')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'stages' in data
    assert len(data['stages']) == 4
    assert data['overall_status'] == 'success'


def test_404_error_handling(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['error'] == 'Not Found'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
