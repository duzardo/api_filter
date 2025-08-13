import re
import json

def extract_message_text(captured_text):
    if not captured_text or captured_text == "null":
        return None
    
    match = re.search(r'mText:\s*([^}]+)', captured_text)
    if match:
        return match.group(1).strip()
    return None

def parse_screen_bounds(screen_bounds_str):
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

def filter_whatsapp_messages(accessibility_events):
    messages = []
    
    for event in accessibility_events:
        if (event.get('nodeId') == 'com.whatsapp:id/message_text' and 
            event.get('Captured Text')):
            
            message_text = extract_message_text(event.get('Captured Text'))
            
            if message_text:
                bounds = parse_screen_bounds(event.get('Screen bounds', ''))
                
                message = {
                    'captured_text': message_text,
                    'event_time': event.get('Event Time'),
                    'node_id': event.get('nodeId'),
                    'screen_bounds': bounds
                }
                
                messages.append(message)
    
    return messages

def process_whatsapp_data(raw_data):
    try:
        if isinstance(raw_data, str):
            raw_data = json.loads(raw_data)
        
        filtered_messages = filter_whatsapp_messages(raw_data.get('events', []))
        
        return {
            'status': 'success',
            'messages_found': len(filtered_messages),
            'messages': filtered_messages
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }
    

with open('example/com_mensagem.txt', 'r') as file:
    data = file.read()

print(process_whatsapp_data(data))