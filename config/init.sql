-- Script de inicialização do banco de dados PostgreSQL
-- Este script é executado automaticamente quando o container é criado

-- Cria o banco de dados se não existir
SELECT 'CREATE DATABASE database_trabalho'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'database_trabalho')\gexec

-- Conecta ao banco de dados
\c database_trabalho;

-- Cria extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Cria a tabela principal de leituras de temperatura
CREATE TABLE IF NOT EXISTS temperature_readings (
    id VARCHAR(255) PRIMARY KEY,
    room_id VARCHAR(255) NOT NULL,
    noted_date TIMESTAMP NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    location_type VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cria índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_room_id ON temperature_readings(room_id);
CREATE INDEX IF NOT EXISTS idx_noted_date ON temperature_readings(noted_date);
CREATE INDEX IF NOT EXISTS idx_temperature ON temperature_readings(temperature);
CREATE INDEX IF NOT EXISTS idx_location_type ON temperature_readings(location_type);
CREATE INDEX IF NOT EXISTS idx_created_at ON temperature_readings(created_at);

-- Cria views para análise de dados
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT 
    room_id as device_id,
    ROUND(AVG(temperature), 2) as avg_temp,
    COUNT(*) as total_readings,
    ROUND(MIN(temperature), 2) as min_temp,
    ROUND(MAX(temperature), 2) as max_temp
FROM temperature_readings
GROUP BY room_id
ORDER BY avg_temp DESC;

CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT 
    EXTRACT(HOUR FROM noted_date) as hora,
    COUNT(*) as contagem,
    ROUND(AVG(temperature), 2) as temp_media
FROM temperature_readings
GROUP BY EXTRACT(HOUR FROM noted_date)
ORDER BY hora;

CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT 
    DATE(noted_date) as data,
    ROUND(MAX(temperature), 2) as temp_max,
    ROUND(MIN(temperature), 2) as temp_min,
    ROUND(AVG(temperature), 2) as temp_media,
    COUNT(*) as total_readings
FROM temperature_readings
GROUP BY DATE(noted_date)
ORDER BY data;

CREATE OR REPLACE VIEW analise_por_tipo_localizacao AS
SELECT 
    location_type,
    COUNT(*) as total_readings,
    ROUND(AVG(temperature), 2) as temp_media,
    ROUND(MIN(temperature), 2) as temp_min,
    ROUND(MAX(temperature), 2) as temp_max,
    ROUND(STDDEV(temperature), 2) as desvio_padrao
FROM temperature_readings
GROUP BY location_type
ORDER BY temp_media DESC;

CREATE OR REPLACE VIEW top_10_temperaturas_altas AS
SELECT 
    id,
    room_id,
    noted_date,
    temperature,
    location_type
FROM temperature_readings
ORDER BY temperature DESC
LIMIT 10;

CREATE OR REPLACE VIEW analise_temporal_mensal AS
SELECT 
    EXTRACT(YEAR FROM noted_date) as ano,
    EXTRACT(MONTH FROM noted_date) as mes,
    COUNT(*) as total_readings,
    ROUND(AVG(temperature), 2) as temp_media,
    ROUND(MIN(temperature), 2) as temp_min,
    ROUND(MAX(temperature), 2) as temp_max
FROM temperature_readings
GROUP BY EXTRACT(YEAR FROM noted_date), EXTRACT(MONTH FROM noted_date)
ORDER BY ano, mes;

-- Mensagem de sucesso
DO $$
BEGIN
    RAISE NOTICE 'Banco de dados database_trabalho inicializado com sucesso!';
    RAISE NOTICE 'Tabelas e views criadas com sucesso!';
END $$;
