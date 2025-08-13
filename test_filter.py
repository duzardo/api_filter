from filter import extract_message_text, parse_screen_bounds, filter_whatsapp_messages

# Dados de teste baseados no arquivo analisado
test_event = {
    'nodeId': 'com.whatsapp:id/message_text',
    'Event Time': '2025-08-13 15:16:42.623408',
    'Captured Text': '{mSpanCount: 0, mSpanData: [], mSpans: [], mText: Olá}',
    'Screen bounds': 'left: 761 - right: 870 - top: 829 - bottom: 908 - width: 109 - height: 79'
}

# Teste individual das funções
print("=== TESTE DAS FUNÇÕES ===")

# Teste extract_message_text
text = extract_message_text(test_event['Captured Text'])
print(f"Texto extraído: '{text}'")

# Teste parse_screen_bounds  
bounds = parse_screen_bounds(test_event['Screen bounds'])
print(f"Coordenadas: {bounds}")

# Teste filter_whatsapp_messages
events = [test_event]
messages = filter_whatsapp_messages(events)
print(f"\nMensagens filtradas: {len(messages)}")
print(f"Primeira mensagem: {messages[0] if messages else 'Nenhuma'}")

print("\n=== RESULTADO FINAL ===")
for msg in messages:
    print(f"Mensagem: {msg['captured_text']}")
    print(f"Horário: {msg['event_time']}")
    print(f"Posição: {msg['screen_bounds']}")