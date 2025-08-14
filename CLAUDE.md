# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

API Flask que processa dados de acessibilidade do Android para extrair mensagens do WhatsApp. Um programa roda em emulador Android usando modo acessibilidade, captura todos os elementos da tela do WhatsApp, envia para esta API que filtra as mensagens reais e armazena no banco de dados.

## System Flow

1. **Programa no Emulador**: Usa modo acessibilidade Android para ler tela do WhatsApp
2. **Captura de Dados**: Retorna array complexo com todos objetos AccessibilityEvent da tela
3. **API de Filtragem**: Recebe array via POST /process
4. **Processamento**: MessageProcessor filtra e processa mensagens
5. **Envio Cromos**: Envia dados para http://192.168.7.100:8090/cromos_forward_return
6. **Persistência**: Se envio bem-sucedido, salva no banco PostgreSQL
7. **Execução**: Roda 24/7 com Waitress para processamento contínuo

## Architecture

- **Framework**: Flask com CORS habilitado
- **Python Version**: 3.11.6
- **Server**: Waitress (produção 24/7)
- **Dependências principais**: Flask, Flask-CORS, requests, waitress, psycopg2
- **Estrutura**: API REST modular com separação de responsabilidades

### File Structure
- **`api_em_app.py`**: Rotas Flask (apenas endpoints)
- **`message_processor.py`**: Módulo principal com lógica de processamento
- **`api_em_db.py`**: Operações de banco de dados PostgreSQL
- **`filter.py`**: Filtros específicos do WhatsApp (formato a definir)
- **`CLAUDE.md`**: Documentação do projeto

## Data Structure (AccessibilityEvent)

Cada objeto AccessibilityEvent contém:
- `mapId`: Identificador único do mapeamento
- `nodeId`: ID do nó (ex: com.whatsapp:id/conversation_text)
- `Package Name`: Nome do app (filtrar por "com.whatsapp")
- `Captured Text`: Texto capturado (onde ficam as mensagens)
- `Event Type`: Tipo de evento de acessibilidade
- `Event Time`: Timestamp do evento
- `Screen bounds`: Coordenadas na tela (left, right, top, bottom)
- `actions`: Ações disponíveis no elemento
- `subNodes`: Array aninhado de sub-elementos (estrutura recursiva)
- Flags: `is Clickable`, `is Focusable`, `is Editable`, etc.

## Development Commands

### Environment Setup
```bash
# Ativar ambiente virtual (Windows)
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### Running the Application
```bash
# Modo desenvolvimento
python api_em_app.py

# Modo produção com Waitress (24/7)
waitress-serve --host=127.0.0.1 --port=5000 api_em_app:app
```

## API Functionality

### Endpoints
- **POST /process**: Recebe dados e processa fluxo completo
- **GET /health**: Verifica se API está funcionando

### Core Features
- **Processamento Modular**: MessageProcessor centraliza toda lógica
- **Envio Cromos**: Integração com endpoint externo para forward de mensagens
- **Banco PostgreSQL**: Persiste mensagens processadas com insertReturnMessages()
- **CORS**: Configurado para requisições cross-origin do emulador
- **Tratamento de Erros**: Logs detalhados de falhas em cada etapa

### Processing Flow
1. **Recebe dados** via POST /process (formato flexível)
2. **MessageProcessor** processa cada mensagem:
   - Envia para Cromos primeiro
   - Se sucesso → salva no banco local
   - Se falha → registra erro
3. **Retorna resultado** com estatísticas detalhadas

### Database Schema
**Tabela**: `api_return_messages`
- `device_id`: ID do dispositivo
- `contact_phone_number`: Número do contato  
- `message_custom_id`: ID único da mensagem
- `message_order`: Ordem de processamento
- `message_schedule`: Timestamp da mensagem

### Cromos Integration
**Endpoint**: `http://192.168.7.100:8090/cromos_forward_return`
**Payload**: JSON com dados da mensagem no formato Cromos

## Filosofia de Desenvolvimento
- Simplicidade: Escrever código simples e direto.
- Legibilidade: Tornar o código fácil de entender.
- Desempenho: Considerar o desempenho sem sacrificar a legibilidade.
- Manutenibilidade: Escrever código que seja fácil de atualizar.
- Testabilidade: Garantir que o código seja testável.
- Menos Código = Menos Dívida: Minimizar a quantidade de código.


## Implementation Status

### ✅ Completed
- **Arquitetura modular** com separação de responsabilidades
- **API Flask** com rotas /process e /health
- **MessageProcessor** para lógica principal de processamento
- **Integração Cromos** via HTTP POST
- **Banco PostgreSQL** com insertReturnMessages corrigido
- **Tratamento de erros** robusto em cada etapa

### 🔄 Pending
- **Filtros específicos** do WhatsApp (aguardando formato exato dos dados)
- **Testes** de integração end-to-end
- **Configuração** do arquivo conn_api.ini para banco
- **Deploy** em produção com Waitress

### 📝 Notes
- Sistema está pronto para receber qualquer formato JSON via /process
- Cromos integration testável independentemente
- Banco de dados configurável via /etc/api_em/conn_api.ini