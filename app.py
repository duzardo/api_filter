import requests
import json
import re
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from psycopg2 import connect
from configparser import ConfigParser


class APIdb:
    """Classe para operações com banco PostgreSQL"""
    
    def __init__(self):
        config = ConfigParser()
        config.read(r"/etc/api_em/conn_api.ini")
        self.conn = connect(
            host=config["db"]["host"],
            port=config["db"]["port"],
            database=config["db"]["database"],
            user=config["Auth"]["user"],
            password=config["Auth"]["password"],
        )

    def cursor(self):
        return self.conn.cursor()

    def insertReturnMessages(
        self,
        device_id,
        contact_phone_number,
        message_custom_id,
        message_order,
        message_schedule,
    ):
        with self.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO api_return_messages (
                    device_id,
                    contact_phone_number,
                    message_custom_id,
                    message_order,
                    message_schedule
                ) VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    device_id,
                    contact_phone_number,
                    message_custom_id,
                    message_order,
                    message_schedule,
                ),
            )
        self.conn.commit()
        cursor.close()


class MessageProcessor:
    """Processador principal de mensagens WhatsApp"""
    
    def __init__(self, cromos_url="http://192.168.7.100:8090/cromos_forward_return"):
        self.cromos_url = cromos_url
        self.db = APIdb()
    
    def extract_message_text(self, captured_text):
        """Extrai texto da mensagem dos dados de acessibilidade"""
        if not captured_text or captured_text == "null":
            return None
        
        match = re.search(r'mText:\s*([^}]+)', captured_text)
        if match:
            return match.group(1).strip()
        return None

    def parse_screen_bounds(self, screen_bounds_str):
        """Parse das coordenadas da tela"""
        if not screen_bounds_str:
            return {}
        
        bounds_match = re.search(r'left:\s*(\d+)\s*-\s*right:\s*(\d+)\s*-\s*top:\s*(\d+)\s*-\s*bottom:\s*(\d+)', screen_bounds_str)
        
        if bounds_match:
            left = int(bounds_match.group(1))
            right = int(bounds_match.group(2))
            top = int(bounds_match.group(3))
            bottom = int(bounds_match.group(4))
            
            return {
                'left': left,
                'right': right,
                'top': top,
                'bottom': bottom,
                'width': right - left,
                'height': bottom - top
            }
        
        return {}

    def filter_whatsapp_messages(self, accessibility_events):
        """Filtra mensagens do WhatsApp dos dados de acessibilidade"""
        messages = []
        
        for event in accessibility_events:
            if (event.get('nodeId') == 'com.whatsapp:id/message_text' and 
                event.get('Captured Text')):
                
                message_text = self.extract_message_text(event.get('Captured Text'))
                
                if message_text:
                    bounds = self.parse_screen_bounds(event.get('Screen bounds', ''))
                    
                    message = {
                        'captured_text': message_text,
                        'event_time': event.get('Event Time'),
                        'node_id': event.get('nodeId'),
                        'screen_bounds': bounds,
                        'phone_number': 'unknown',  # Será extraído ou configurado
                        'contact_phone_number': 'unknown',
                        'message_custom_id': f"msg_{datetime.now().timestamp()}",
                        'schedule': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    messages.append(message)
        
        return messages
    
    def send_to_cromos(self, message_data):
        """Envia mensagem para o endpoint Cromos"""
        try:
            response = requests.post(
                self.cromos_url,
                json=message_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                return {"success": True, "error": None}
            else:
                return {
                    "success": False, 
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Timeout ao conectar com Cromos"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Erro de conexão com Cromos"}
        except Exception as e:
            return {"success": False, "error": f"Erro inesperado: {str(e)}"}
    
    def process_accessibility_data(self, raw_data):
        """Processa dados de acessibilidade: filtra WhatsApp, envia Cromos, salva BD"""
        try:
            processed_messages = []
            errors = []
            
            # Primeiro, filtra mensagens do WhatsApp se dados são de acessibilidade
            if isinstance(raw_data, dict) and 'events' in raw_data:
                # Dados de acessibilidade - aplicar filtros WhatsApp
                filtered_messages = self.filter_whatsapp_messages(raw_data['events'])
                messages_to_process = filtered_messages
            elif isinstance(raw_data, list):
                # Array de mensagens já processadas
                messages_to_process = raw_data
            elif isinstance(raw_data, dict) and 'messages' in raw_data:
                # Objeto com array de mensagens
                messages_to_process = raw_data['messages']
            else:
                # Mensagem única
                messages_to_process = [raw_data]
            
            for idx, message_data in enumerate(messages_to_process):
                try:
                    # 1. Envia para Cromos primeiro
                    cromos_result = self.send_to_cromos(message_data)
                    
                    if cromos_result['success']:
                        # 2. Se envio para Cromos foi bem-sucedido, salva no banco local
                        device_id = message_data.get('phone_number', 'unknown')
                        contact_phone = message_data.get('contact_phone_number', 'unknown')
                        custom_id = message_data.get('message_custom_id', f'msg_{idx}_{datetime.now().timestamp()}')
                        order = idx + 1
                        schedule = message_data.get('schedule', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        
                        # Salva no banco local
                        self.db.insertReturnMessages(
                            device_id=device_id,
                            contact_phone_number=contact_phone,
                            message_custom_id=custom_id,
                            message_order=order,
                            message_schedule=schedule
                        )
                        
                        processed_messages.append({
                            'message_id': custom_id,
                            'status': 'success',
                            'cromos_sent': True,
                            'saved_to_db': True,
                            'message_text': message_data.get('captured_text', '')
                        })
                    else:
                        # Falha no envio para Cromos
                        errors.append({
                            'message_id': message_data.get('message_custom_id', f'msg_{idx}'),
                            'error': f'Falha ao enviar para Cromos: {cromos_result["error"]}'
                        })
                        
                except Exception as msg_error:
                    errors.append({
                        'message_id': message_data.get('message_custom_id', f'msg_{idx}'),
                        'error': f'Erro no processamento: {str(msg_error)}'
                    })
            
            return {
                'status': 'completed',
                'total_messages': len(messages_to_process),
                'successful': len(processed_messages),
                'failed': len(errors),
                'processed_messages': processed_messages,
                'errors': errors
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': f'Erro geral no processamento: {str(e)}'
            }


# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Instância global do processador
processor = MessageProcessor()


@app.route('/process', methods=['POST'])
def process_accessibility_data():
    """Processa dados de acessibilidade e envia para Cromos + salva no banco"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Nenhum dado fornecido'}), 400
        
        # Processa dados
        result = processor.process_accessibility_data(data)
        
        # Retorna resultado
        if result['status'] == 'error':
            return jsonify(result), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Erro no processamento: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    try:
        # Testa conexão com banco
        cursor = processor.db.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        
        return jsonify({
            'status': 'API funcionando',
            'version': '2.0',
            'database': 'conectado',
            'cromos_endpoint': processor.cromos_url
        })
    except Exception as e:
        return jsonify({
            'status': 'API funcionando',
            'version': '2.0',
            'database': f'erro: {str(e)}',
            'cromos_endpoint': processor.cromos_url
        }), 206


if __name__ == '__main__':
    # Desenvolvimento
    app.run(host='127.0.0.1', port=5000, debug=True)