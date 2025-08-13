# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

API Flask que processa dados de acessibilidade do Android para extrair mensagens do WhatsApp. Um programa roda em emulador Android usando modo acessibilidade, captura todos os elementos da tela do WhatsApp, envia para esta API que filtra as mensagens reais e armazena no banco de dados.

## System Flow

1. **Programa no Emulador**: Usa modo acessibilidade Android para ler tela do WhatsApp
2. **Captura de Dados**: Retorna array complexo com todos objetos AccessibilityEvent da tela
3. **API de Filtragem**: Recebe array, filtra mensagens relevantes do WhatsApp
4. **Persistência**: Armazena mensagens filtradas no banco de dados
5. **Execução**: Roda 24/7 com Waitress para processamento contínuo

## Architecture

- **Framework**: Flask com CORS habilitado
- **Python Version**: 3.11.6
- **Server**: Waitress (produção 24/7)
- **Dependências principais**: Flask, Flask-CORS, requests, waitress
- **Estrutura**: API REST para processamento de dados de acessibilidade

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
python api_app.py

# Modo produção com Waitress (24/7)
waitress-serve --host=127.0.0.1 --port=5000 api_app:app
```

## API Functionality

### Core Features
- **POST /process**: Recebe array de AccessibilityEvent objects
- **Filtros de WhatsApp**: Identifica elementos com Package Name "com.whatsapp"
- **Extração de Mensagens**: Filtra objetos com Captured Text não nulo
- **Processamento Recursivo**: Navega em subNodes para encontrar mensagens aninhadas
- **Persistência**: Armazena mensagens extraídas no banco de dados
- **CORS**: Configurado para requisições cross-origin do emulador

### Filtering Logic
1. Filtrar por Package Name = "com.whatsapp"
2. Verificar se Captured Text não é null/vazio
3. Processar subNodes recursivamente
4. Identificar elementos de mensagem (textos, timestamps, remetentes)
5. Estruturar dados antes de salvar no BD

## Filosofia de Desenvolvimento
- Simplicidade: Escrever código simples e direto.
- Legibilidade: Tornar o código fácil de entender.
- Desempenho: Considerar o desempenho sem sacrificar a legibilidade.
- Manutenibilidade: Escrever código que seja fácil de atualizar.
- Testabilidade: Garantir que o código seja testável.
- Menos Código = Menos Dívida: Minimizar a quantidade de código.


## Important Notes

- O arquivo principal (`api_app.py`) está em desenvolvimento inicial
- Necessário implementar rotas, filtros e conexão com banco de dados
- CORS já configurado para aceitar requisições de diferentes origens