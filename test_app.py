import pytest
import os
from unittest.mock import patch, MagicMock

# Mock de Anthropic antes de importar app
@pytest.fixture(autouse=True)
def mock_anthropic():
    """Mock global de Anthropic para todos los tests"""
    with patch('anthropic.Anthropic') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance

# Ahora importamos app después del mock
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

@patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'})
def test_chat_endpoint_with_mock(client, mock_anthropic):
    """Test: Verificar que el endpoint de chat funciona con mock"""
    # Configurar el mock para simular respuesta de Claude
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Esta es una respuesta de prueba")]
    mock_anthropic.messages.create.return_value = mock_response
    
    response = client.post('/chat', 
                          json={'message': 'test message'},
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
    assert data['student'] == 'Eras'

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