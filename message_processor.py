import requests
import json
from datetime import datetime
from api_em_db import APIdb
from filter import process_whatsapp_data


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
                        # Extrai campos necessários (usa valores padrão se não existirem)
                        device_id = message_data.get('phone_number', 'unknown')
                        contact_phone = message_data.get('contact_phone_number', 'unknown')
                        custom_id = message_data.get('message_custom_id', f'msg_{idx}')
                        order = idx + 1
                        schedule = message_data.get('schedule', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        
                        # Salva no banco local
                        self.db.insertReturnMessages(
                            device_id=device_id,
                            contact_phone_number=contact_phone,
                            message_custom_id=custom_id,
                            message_order=order,
                            message_schedule=schedule,
                            readed_at_schedule=schedule,  # mesmo valor do schedule
                            returned=True,                # foi processado com sucesso
                            returned_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
        # Por enquanto, chama a função existente do filter.py
        # Quando soubermos o formato exato, podemos expandir aqui
        return process_whatsapp_data(accessibility_data)