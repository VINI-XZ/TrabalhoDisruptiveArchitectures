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

<img width="1909" height="915" alt="Temperatura 3" src="https://github.com/user-attachments/assets/5756a86f-45d9-4439-8da5-ba6db8e5b67d" />

<img width="1920" height="925" alt="Temperatura 2" src="https://github.com/user-attachments/assets/1318e550-86f4-4efe-b8a1-f3410b535274" />

<img width="1903" height="920" alt="Temperatura 1" src="https://github.com/user-attachments/assets/57d614c8-1f77-4860-a0a9-fc18627e1fe3" />



