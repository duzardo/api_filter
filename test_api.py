import requests
import json

# Dados de teste simulando o que viria do emulador
test_data = {
    "events": [
        {
            "nodeId": "com.whatsapp:id/message_text",
            "Event Time": "2025-08-13 15:16:42.623408",
            "Captured Text": "{mSpanCount: 0, mSpanData: [], mSpans: [], mText: Olá}",
            "Screen bounds": "left: 761 - right: 870 - top: 829 - bottom: 908 - width: 109 - height: 79"
        },
        {
            "nodeId": "com.whatsapp:id/message_text", 
            "Event Time": "2025-08-13 15:16:42.623434",
            "Captured Text": "{mSpanCount: 0, mSpanData: [], mSpans: [], mText: Tudo bem?}",
            "Screen bounds": "left: 200 - right: 400 - top: 500 - bottom: 600 - width: 200 - height: 100"
        },
        {
            "nodeId": "android:id/statusBarBackground",
            "Event Time": "2025-08-13 15:16:36.222075",
            "Captured Text": "null",
            "Screen bounds": "left: -140 - right: 939 - top: 0 - bottom: 94 - width: 1079 - height: 94"
        }
    ]
}

def test_api():
    url = "http://127.0.0.1:5000"
    
    # Teste health check
    print("=== TESTE HEALTH CHECK ===")
    try:
        response = requests.get(f"{url}/health")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}")
    except Exception as e:
        print(f"Erro no health check: {e}")
    
    print("\n=== TESTE PROCESS ===")
    try:
        response = requests.post(f"{url}/process", 
                               json=test_data,
                               headers={'Content-Type': 'application/json'})
        
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Mensagens encontradas: {result.get('messages_found', 0)}")
        
        for i, msg in enumerate(result.get('messages', [])):
            print(f"\nMensagem {i+1}:")
            print(f"  Texto: {msg['captured_text']}")
            print(f"  Horário: {msg['event_time']}")
            print(f"  Posição: {msg['screen_bounds']}")
            
    except Exception as e:
        print(f"Erro no teste: {e}")

if __name__ == "__main__":
    test_api()