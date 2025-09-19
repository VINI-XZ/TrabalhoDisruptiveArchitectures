# 🌡️ Pipeline de Dados IoT - Análise de Temperaturas

## 📋 Sobre o Projeto

Este projeto implementa um **pipeline completo de dados IoT** que processa leituras de temperatura de sensores conectados, armazenando os dados em PostgreSQL e fornecendo visualizações interativas através de um dashboard Streamlit.

### 🎯 Objetivo
Criar um sistema robusto para análise de dados de temperatura coletados por dispositivos IoT, permitindo insights sobre padrões temporais, comparação entre dispositivos e identificação de anomalias.

## 🚀 Tutorial de Execução

### ✅ Pré-requisitos
- Python 3.11+ instalado
- Docker e Docker Compose instalados
- Arquivo `IOT-temp.csv` no diretório do projeto

### 📋 Passo a Passo

#### 1️⃣ **Instalar Dependências**
```bash
pip install -r requirements.txt
```

#### 2️⃣ **Iniciar PostgreSQL**
```bash
docker-compose up -d postgres-iot
```

#### 3️⃣ **Aguardar PostgreSQL Inicializar**
```bash
# Aguarde aproximadamente 10 segundos
Start-Sleep -Seconds 10
```

#### 4️⃣ **Processar Dados CSV**
```bash
py iot_data_processor.py
```

#### 5️⃣ **Iniciar Dashboard**
```bash
py -m streamlit run dashboard.py
```

#### 6️⃣ **Acessar Dashboard**
- Abra seu navegador
- Acesse: **http://localhost:8501**

### 🔧 Comandos Alternativos

#### **Execução com Script Automatizado**
```bash
py run_pipeline.py
```

#### **Execução com Docker Compose Completo**
```bash
docker-compose up -d
```

#### **Verificar Status dos Serviços**
```bash
# PostgreSQL
docker ps | grep postgres

# Dashboard
netstat -an | findstr :8501
```

### 📊 Principais Descobertas
- **Volume de dados**: 87.606 leituras processadas com sucesso
- **Período de coleta**: 4 meses (julho a novembro de 2018)
- **Padrões temporais**: Variações significativas entre horários
- **Ambientes**: Diferenças entre leituras internas e externas
- **Temperaturas**: Range de valores com identificação de extremos

### 🎯 Aplicações Práticas
- **Monitoramento de infraestrutura**: Detecção de falhas em sistemas
- **Análise de comportamento**: Padrões de uso dos ambientes
- **Manutenção preditiva**: Identificação de tendências
- **Otimização energética**: Correlação temperatura vs. consumo

## 📚 Tecnologias Utilizadas

- **Python 3.11+**: Linguagem principal
- **Pandas**: Processamento de dados
- **SQLAlchemy**: ORM para PostgreSQL
- **Streamlit**: Framework web para dashboard
- **Plotly**: Visualizações interativas
- **PostgreSQL 15**: Banco de dados relacional
- **Docker**: Containerização
- **Docker Compose**: Orquestração de serviços


