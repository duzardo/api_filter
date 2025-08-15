import requests
import json
import re
from datetime import datetime
from api_em_db import APIdb


def extract_message_text(captured_text):
    if not captured_text or captured_text == "null":
        return None
    
    match = re.search(r"mText:\s*([^}]+)", captured_text)
    if match:
        return match.group(1).strip()
    return None


def parse_screen_bounds(screen_bounds_str):
    if not screen_bounds_str:
        return {}

    bounds_match = re.search(
        r"left:\s*(\d+)\s*-\s*right:\s*(\d+)\s*-\s*top:\s*(\d+)\s*-\s*bottom:\s*(\d+)",
        screen_bounds_str,
    )

    if bounds_match:
        left = int(bounds_match.group(1))
        right = int(bounds_match.group(2))
        top = int(bounds_match.group(3))
        bottom = int(bounds_match.group(4))

        return {
            "left": left,
            "right": right,
            "top": top,
            "bottom": bottom,
            "width": right - left,
            "height": bottom - top,
        }

    return {}


def filter_whatsapp_messages(accessibility_events):
    messages = []

    for event in accessibility_events:
        if event.get("nodeId") == "com.whatsapp:id/message_text" and event.get(
            "Captured Text"
        ):

            message_text = extract_message_text(event.get("Captured Text"))

            if message_text:
                bounds = parse_screen_bounds(event.get("Screen bounds", ""))

                message = {
                    "captured_text": message_text,
                    "event_time": event.get("Event Time"),
                    "node_id": event.get("nodeId"),
                    "screen_bounds": bounds,
                }

                messages.append(message)

    return messages


def process_whatsapp_data(raw_data):
    try:
        if isinstance(raw_data, str):
            raw_data = json.loads(raw_data)

        filtered_messages = filter_whatsapp_messages(raw_data.get("events", []))

        return {
            "status": "success",
            "messages_found": len(filtered_messages),
            "messages": filtered_messages,
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


class MessageProcessor:
    def __init__(self, cromos_url="http://192.168.7.100:8090/cromos_forward_return"):
        self.cromos_url = cromos_url
        self.db = APIdb()
    
    def send_to_cromos(self, message_data):
        """
        Envia mensagem para o endpoint Cromos
        
        Args:
            message_data (dict): Dados da mensagem no formato Cromos
        
        Returns:
            dict: {"success": bool, "error": str or None}
        """
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
        """
        Processa dados de acessibilidade completos: filtra, envia para Cromos e salva no banco
        
        Args:
            raw_data: Dados brutos recebidos da API
            
        Returns:
            dict: Resultado do processamento com estatísticas
        """
        try:
            processed_messages = []
            errors = []
            
            # Determina formato dos dados de entrada
            if isinstance(raw_data, list):
                messages_to_process = raw_data
            elif isinstance(raw_data, dict) and 'messages' in raw_data:
                messages_to_process = raw_data['messages']
            else:
                messages_to_process = [raw_data]  # Trata como mensagem única
            
            for idx, message_data in enumerate(messages_to_process):
                try:
                    # 1. Envia para Cromos primeiro
                    cromos_result = self.send_to_cromos(message_data)
                    
                    if cromos_result['success']:
                        # 2. Se envio para Cromos foi bem-sucedido, salva no banco local
                        # Campos que virão dos dados reais
                        device_id = message_data.get('device_id', 'UNKNOWN_DEVICE')
                        contact_phone = message_data.get('contact_phone_number', 'UNKNOWN_CONTACT')
                        returned = message_data.get('returned', True)
                        returned_at = message_data.get('returned_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        
                        # Campos gerados automaticamente
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        custom_id = f"{device_id}_{int(datetime.now().timestamp())}_{idx}"
                        order = idx + 1
                        schedule = current_time
                        
                        # Salva no banco local
                        self.db.insertReturnMessages(
                            device_id=device_id,
                            contact_phone_number=contact_phone,
                            message_custom_id=custom_id,
                            message_order=order,
                            message_schedule=schedule,
                            readed_at_schedule=current_time,
                            returned=returned,
                            returned_at=returned_at
                        )
                        
                        processed_messages.append({
                            'message_id': custom_id,
                            'status': 'success',
                            'cromos_sent': True,
                            'saved_to_db': True
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
    
    def filter_whatsapp_messages(self, accessibility_data):
        """
        Aplica filtros específicos do WhatsApp nos dados de acessibilidade
        
        Args:
            accessibility_data: Dados de acessibilidade brutos
            
        Returns:
            dict: Dados filtrados prontos para processamento
        """
        return process_whatsapp_data(accessibility_data)