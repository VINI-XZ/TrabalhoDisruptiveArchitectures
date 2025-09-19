# 🚀 Guia de Execução Rápida

## ⚡ Execução em 3 Passos

### 1️⃣ Preparar o Ambiente
```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar PostgreSQL
docker-compose up -d postgres-iot
```

### 2️⃣ Processar Dados
```bash
# Executar pipeline completo
python iot_data_processor.py
```

### 3️⃣ Visualizar Dashboard
```bash
# Iniciar dashboard
streamlit run dashboard.py
```

**Acesse**: http://localhost:8501

---

## 🎯 Execução Automatizada

### Opção 1: Script Interativo
```bash
python run_pipeline.py
```

### Opção 2: Setup Completo
```bash
python setup.py
```

---

## 📊 Verificação Rápida

### Status dos Serviços
```bash
# PostgreSQL
docker ps | grep postgres

# Dashboard (em outro terminal)
curl http://localhost:8501
```

### Estatísticas do Banco
```bash
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://postgres:admin@localhost:5432/database_trabalho')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM temperature_readings')
print(f'Total de registros: {cursor.fetchone()[0]:,}')
conn.close()
"
```

---

## 🛑 Parar Serviços

```bash
# Parar todos os containers
docker-compose down

# Parar apenas PostgreSQL
docker stop postgres-iot
```

---

## 📁 Arquivos Principais

- `iot_data_processor.py` - Processamento de dados
- `dashboard.py` - Dashboard Streamlit
- `docker-compose.yml` - Orquestração Docker
- `requirements.txt` - Dependências Python
- `README.md` - Documentação completa

---

## 🔧 Troubleshooting

### PostgreSQL não conecta
```bash
docker logs postgres-iot
docker restart postgres-iot
```

### Dashboard não carrega
```bash
# Verificar porta
netstat -an | grep 8501

# Reiniciar Streamlit
streamlit run dashboard.py --server.port 8502
```

### Erro de dependências
```bash
pip install --upgrade -r requirements.txt
```
