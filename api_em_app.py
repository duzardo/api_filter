from flask import Flask, request, jsonify
from flask_cors import CORS
from configparser import ConfigParser
from api_em_db import APIdb
from filter import process_whatsapp_data

app = Flask(__name__)
CORS(app)

@app.route('/process', methods=['POST'])
def process_accessibility_data():
    """Processa dados de acessibilidade e filtra mensagens do WhatsApp"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Nenhum dado fornecido'}), 400
        
        # Processa e filtra mensagens do WhatsApp
        result = process_whatsapp_data(data)
        
        if result['status'] == 'error':
            return jsonify(result), 500
        
        # TODO: Salvar no banco de dados usando APIdb
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Erro no processamento: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({'status': 'API funcionando', 'version': '1.0'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
