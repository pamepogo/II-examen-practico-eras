import pytest
from app import app

@pytest.fixture
def client():
    """Fixture para crear un cliente de prueba"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test: Verificar que la ruta principal funciona"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Eras' in response.data
    assert b'Flask con IA' in response.data

def test_health_endpoint(client):
    """Test: Verificar endpoint de salud"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['student'] == 'Eras'
    assert data['version'] == '1.0.5'

def test_saludo_route(client):
    """Test: Verificar ruta de saludo con parámetro"""
    response = client.get('/saludo/DevOps')
    assert response.status_code == 200
    assert b'Hola DevOps' in response.data
    assert b'eras.byronrm.com' in response.data

def test_chat_endpoint_exists(client):
    """Test: Verificar que el endpoint de chat existe"""
    response = client.post('/chat', 
                          json={'message': 'test'},
                          content_type='application/json')
    # Puede ser 200 (con API key) o 500 (sin API key en tests)
    assert response.status_code in [200, 500]

def test_chat_without_message(client):
    """Test: Verificar manejo de errores cuando no hay mensaje"""
    response = client.post('/chat', 
                          json={},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_chat_with_invalid_json(client):
    """Test: Verificar manejo de JSON inválido"""
    response = client.post('/chat', 
                          data='invalid json',
                          content_type='application/json')
    assert response.status_code in [400, 500]