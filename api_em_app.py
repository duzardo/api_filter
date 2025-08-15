from flask import Flask, request, jsonify
from flask_cors import CORS
from message_processor import MessageProcessor

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route("/process", methods=["POST"])
def process_accessibility_data():
    """Processa dados de acessibilidade e envia para Cromos + salva no banco"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Nenhum dado fornecido"}), 400

        # Delega todo processamento para MessageProcessor
        processor = MessageProcessor()
        result = processor.process_accessibility_data(data)

        # Retorna resultado do processamento
        if result["status"] == "error":
            return jsonify(result), 500

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Erro no processamento: {str(e)}"}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({"status": "API funcionando", "version": "1.0"})


def create_app():
    return app
