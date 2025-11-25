from flask import Flask, request, jsonify, render_template_string
from anthropic import Anthropic
import os

app = Flask(__name__)

# Inicializar cliente de Anthropic (Claude AI)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Template HTML simple
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Eras - Con IA DevOps</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #2c3e50; }
        .container { background: #ecf0f1; padding: 20px; border-radius: 8px; }
        input[type="text"] { width: 70%; padding: 10px; }
        button { padding: 10px 20px; background: #3498db; color: white; border: none; cursor: pointer; }
        button:hover { background: #2980b9; }
        #response { margin-top: 20px; background: white; padding: 15px; border-radius: 5px; min-height: 100px; }
    </style>
</head>
<body>
    <h1> Aplicación Flask con IA - Eras</h1>
    <div class="container">
        <h2>Chat AI</h2>
        <input type="text" id="message" placeholder="Escribe tu mensaje aquí...">
        <button onclick="sendMessage()">Enviar</button>
        <div id="response"></div>
    </div>
    
    <script>
        async function sendMessage() {
            const message = document.getElementById('message').value;
            const responseDiv = document.getElementById('response');
            
            if (!message) {
                alert('Por favor escribe un mensaje');
                return;
            }
            
            responseDiv.innerHTML = 'Procesando...';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    responseDiv.innerHTML = '<strong>Claude:</strong> ' + data.response;
                } else {
                    responseDiv.innerHTML = '<strong>Error:</strong> ' + data.error;
                }
            } catch (error) {
                responseDiv.innerHTML = '<strong>Error:</strong> ' + error.message;
            }
        }
        
        document.getElementById('message').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    """Endpoint de salud para verificar que la app está funcionando"""
    return jsonify({
        "status": "healthy",
        "student": "Eras",
        "version": "1.0.5"
    })

@app.route('/saludo/<nombre>')
def saludo(nombre):
    return f"<h2>Hola {nombre}, bienvenido a eras.byronrm.com 🚀</h2>"

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint para chatear AI"""
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({"error": "No se proporcionó ningún mensaje"}), 400
        
        # Llamar a la API de Claude
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": message}]
        )
        
        return jsonify({
            "response": response.content[0].text,
            "student": "Eras"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)