#!/usr/bin/env python3
"""
Pipeline de Dados IoT - Processamento de Leituras de Temperatura
Este script processa dados de temperatura de dispositivos IoT e armazena no PostgreSQL
"""

import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import logging
from datetime import datetime
import sys
import os

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/iot_pipeline.log' if os.path.exists('logs') else '../logs/iot_pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class IoTDataProcessor:
    def __init__(self, db_config):
        """
        Inicializa o processador de dados IoT
        
        Args:
            db_config (dict): Configurações do banco de dados
        """
        self.db_config = db_config
        self.engine = None
        # Define o caminho do CSV baseado no contexto (local ou Docker)
        if os.path.exists('data/IOT-temp.csv'):
            self.csv_file = 'data/IOT-temp.csv'  # Para Docker
        else:
            self.csv_file = '../data/IOT-temp.csv'  # Para execução local
        
    def connect_database(self):
        """Estabelece conexão com o PostgreSQL"""
        try:
            # String de conexão
            connection_string = (
                f"postgresql://{self.db_config['user']}:{self.db_config['password']}"
                f"@{self.db_config['host']}:{self.db_config['port']}"
                f"/{self.db_config['database']}"
            )
            
            self.engine = create_engine(connection_string)
            
            # Testa a conexão
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                logging.info("✅ Conexão com PostgreSQL estabelecida com sucesso!")
                return True
                
        except Exception as e:
            logging.error(f"❌ Erro ao conectar com PostgreSQL: {e}")
            return False
    
    def create_tables(self):
        """Cria as tabelas necessárias no banco de dados"""
        try:
            with self.engine.connect() as conn:
                # Cria tabela de leituras de temperatura
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS temperature_readings (
                    id VARCHAR(255) PRIMARY KEY,
                    room_id VARCHAR(255) NOT NULL,
                    noted_date TIMESTAMP NOT NULL,
                    temperature DECIMAL(5,2) NOT NULL,
                    location_type VARCHAR(10) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
                
                conn.execute(text(create_table_sql))
                conn.commit()
                logging.info("✅ Tabela 'temperature_readings' criada com sucesso!")
                
                # Cria índices para melhor performance
                indexes_sql = [
                    "CREATE INDEX IF NOT EXISTS idx_room_id ON temperature_readings(room_id);",
                    "CREATE INDEX IF NOT EXISTS idx_noted_date ON temperature_readings(noted_date);",
                    "CREATE INDEX IF NOT EXISTS idx_temperature ON temperature_readings(temperature);",
                    "CREATE INDEX IF NOT EXISTS idx_location_type ON temperature_readings(location_type);"
                ]
                
                for index_sql in indexes_sql:
                    conn.execute(text(index_sql))
                
                conn.commit()
                logging.info("✅ Índices criados com sucesso!")
                
        except Exception as e:
            logging.error(f"❌ Erro ao criar tabelas: {e}")
            return False
        
        return True
    
    def load_and_process_csv(self):
        """Carrega e processa o arquivo CSV"""
        try:
            logging.info(f"📂 Carregando arquivo CSV: {self.csv_file}")
            
            # Lê o CSV em chunks para economizar memória
            chunk_size = 10000
            total_rows = 0
            
            # Primeiro, vamos contar o total de linhas
            with open(self.csv_file, 'r') as f:
                total_rows = sum(1 for line in f) - 1  # -1 para excluir header
            
            logging.info(f"📊 Total de registros no CSV: {total_rows:,}")
            
            processed_chunks = 0
            
            # Processa o CSV em chunks
            for chunk in pd.read_csv(self.csv_file, chunksize=chunk_size):
                try:
                    # Renomeia colunas para padronizar
                    chunk.columns = ['id', 'room_id', 'noted_date', 'temperature', 'location_type']
                    
                    # Converte a data para formato timestamp
                    chunk['noted_date'] = pd.to_datetime(chunk['noted_date'], format='%d-%m-%Y %H:%M')
                    
                    # Remove linhas com dados inválidos
                    chunk = chunk.dropna()
                    chunk = chunk[chunk['temperature'].notna()]
                    
                    # Insere no banco de dados
                    chunk.to_sql(
                        'temperature_readings',
                        self.engine,
                        if_exists='append',
                        index=False,
                        method='multi'
                    )
                    
                    processed_chunks += 1
                    records_processed = processed_chunks * chunk_size
                    progress = min(100, (records_processed / total_rows) * 100)
                    
                    logging.info(f"📈 Progresso: {progress:.1f}% - {records_processed:,} registros processados")
                    
                except Exception as e:
                    logging.error(f"❌ Erro ao processar chunk: {e}")
                    continue
            
            logging.info("✅ Arquivo CSV processado com sucesso!")
            return True
            
        except FileNotFoundError:
            logging.error(f"❌ Arquivo {self.csv_file} não encontrado!")
            return False
        except Exception as e:
            logging.error(f"❌ Erro ao processar CSV: {e}")
            return False
    
    def create_views(self):
        """Cria views SQL para análise de dados"""
        try:
            with self.engine.connect() as conn:
                views_sql = {
                    'avg_temp_por_dispositivo': """
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
                    """,
                    
                    'leituras_por_hora': """
                        CREATE OR REPLACE VIEW leituras_por_hora AS
                        SELECT 
                            EXTRACT(HOUR FROM noted_date) as hora,
                            COUNT(*) as contagem,
                            ROUND(AVG(temperature), 2) as temp_media
                        FROM temperature_readings
                        GROUP BY EXTRACT(HOUR FROM noted_date)
                        ORDER BY hora;
                    """,
                    
                    'temp_max_min_por_dia': """
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
                    """,
                    
                    'analise_por_tipo_localizacao': """
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
                    """,
                    
                    'top_10_temperaturas_altas': """
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
                    """,
                    
                    'analise_temporal_mensal': """
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
                    """
                }
                
                for view_name, view_sql in views_sql.items():
                    conn.execute(text(view_sql))
                    logging.info(f"✅ View '{view_name}' criada com sucesso!")
                
                conn.commit()
                logging.info("✅ Todas as views foram criadas com sucesso!")
                
        except Exception as e:
            logging.error(f"❌ Erro ao criar views: {e}")
            return False
        
        return True
    
    def get_database_stats(self):
        """Obtém estatísticas do banco de dados"""
        try:
            with self.engine.connect() as conn:
                # Conta total de registros
                result = conn.execute(text("SELECT COUNT(*) FROM temperature_readings"))
                total_records = result.fetchone()[0]
                
                # Obtém range de datas
                result = conn.execute(text("""
                    SELECT 
                        MIN(noted_date) as data_min,
                        MAX(noted_date) as data_max,
                        COUNT(DISTINCT room_id) as total_dispositivos
                    FROM temperature_readings
                """))
                stats = result.fetchone()
                
                logging.info("📊 Estatísticas do Banco de Dados:")
                logging.info(f"   • Total de registros: {total_records:,}")
                logging.info(f"   • Período: {stats[0]} até {stats[1]}")
                logging.info(f"   • Total de dispositivos: {stats[2]}")
                
        except Exception as e:
            logging.error(f"❌ Erro ao obter estatísticas: {e}")
    
    def run_pipeline(self):
        """Executa o pipeline completo"""
        logging.info("🚀 Iniciando Pipeline de Dados IoT")
        logging.info("=" * 50)
        
        # 1. Conecta ao banco
        if not self.connect_database():
            return False
        
        # 2. Cria tabelas
        if not self.create_tables():
            return False
        
        # 3. Processa CSV
        if not self.load_and_process_csv():
            return False
        
        # 4. Cria views
        if not self.create_views():
            return False
        
        # 5. Mostra estatísticas
        self.get_database_stats()
        
        logging.info("=" * 50)
        logging.info("✅ Pipeline executado com sucesso!")
        return True

def main():
    """Função principal"""
    # Configurações do banco de dados
    db_config = {
        'host': 'localhost',
        'port': '5432',
        'database': 'database_trabalho',
        'user': 'postgres',
        'password': 'admin'
    }
    
    # Cria e executa o pipeline
    processor = IoTDataProcessor(db_config)
    
    if processor.run_pipeline():
        print("\n🎉 Pipeline de dados IoT executado com sucesso!")
        print("📊 Dados processados e armazenados no PostgreSQL")
        print("📈 Views SQL criadas para análise")
        print("🔍 Execute o dashboard Streamlit para visualizar os dados")
    else:
        print("\n❌ Erro ao executar o pipeline")
        sys.exit(1)

if __name__ == "__main__":
    main()
