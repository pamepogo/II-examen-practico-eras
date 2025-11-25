import pytest
import os
from unittest.mock import patch, MagicMock
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

def test_chat_without_message(client):
    """Test: Verificar manejo de errores cuando no hay mensaje"""
    response = client.post('/chat', 
                          json={},
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_chat_without_api_key(client):
    """Test: Verificar que sin API key retorna error 500"""
    with patch.dict(os.environ, {}, clear=True):
        # Limpiar el cache del cliente si existe
        if hasattr(app, 'get_anthropic_client'):
            if hasattr(app.get_anthropic_client, 'client'):
                delattr(app.get_anthropic_client, 'client')
        
        response = client.post('/chat', 
                              json={'message': 'test'},
                              content_type='application/json')
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

@patch('app.get_anthropic_client')
def test_chat_endpoint_with_mock(mock_get_client, client):
    """Test: Verificar que el endpoint de chat funciona con mock"""
    # Crear un mock del cliente de Anthropic
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Esta es una respuesta de prueba")]
    mock_client.messages.create.return_value = mock_response
    mock_get_client.return_value = mock_client
    
    response = client.post('/chat', 
                          json={'message': 'test message'},
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
    assert data['student'] == 'Eras'
    assert data['response'] == "Esta es una respuesta de prueba"