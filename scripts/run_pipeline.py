#!/usr/bin/env python3
"""
Script de Execução Rápida - Pipeline de Dados IoT
Este script executa o pipeline completo de forma simplificada
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def print_banner():
    """Imprime banner do projeto"""
    print("=" * 60)
    print("🌡️  PIPELINE DE DADOS IoT - TEMPERATURAS")
    print("=" * 60)
    print("📊 Processamento de dados de sensores IoT")
    print("🗄️  Armazenamento em PostgreSQL")
    print("📈 Dashboard interativo com Streamlit")
    print("=" * 60)

def check_requirements():
    """Verifica se todos os requisitos estão atendidos"""
    print("\n🔍 Verificando requisitos...")
    
    # Verifica se o arquivo CSV existe
    csv_file = Path("../data/IOT-temp.csv")
    if not csv_file.exists():
        print("❌ Arquivo IOT-temp.csv não encontrado!")
        return False
    print(f"✅ Arquivo CSV encontrado: {csv_file.stat().st_size / (1024*1024):.1f} MB")
    
    # Verifica se o PostgreSQL está rodando
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=postgres-iot", "--format", "{{.Status}}"],
            capture_output=True, text=True, check=True
        )
        if "Up" in result.stdout:
            print("✅ PostgreSQL está rodando")
        else:
            print("❌ PostgreSQL não está rodando. Execute: docker-compose up -d postgres-iot")
            return False
    except subprocess.CalledProcessError:
        print("❌ Docker não está disponível")
        return False
    
    return True

def run_data_processing():
    """Executa o processamento de dados"""
    print("\n📊 Iniciando processamento de dados...")
    print("⏳ Isso pode levar alguns minutos devido ao volume de dados...")
    
    try:
        result = subprocess.run(
            [sys.executable, "../src/iot_data_processor.py"],
            check=True,
            capture_output=True,
            text=True
        )
        
        print("✅ Processamento concluído com sucesso!")
        
        # Mostra algumas estatísticas da saída
        lines = result.stdout.split('\n')
        for line in lines:
            if "Total de registros:" in line or "Dispositivos:" in line:
                print(f"   {line}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no processamento: {e}")
        if e.stderr:
            print(f"Erro: {e.stderr}")
        return False

def start_dashboard():
    """Inicia o dashboard Streamlit"""
    print("\n🚀 Iniciando dashboard Streamlit...")
    print("📱 Dashboard será acessível em: http://localhost:8501")
    
    try:
        # Inicia o Streamlit em background
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "../src/dashboard.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
        
        print("✅ Dashboard iniciado com sucesso!")
        print("\n📋 Instruções:")
        print("1. Abra seu navegador")
        print("2. Acesse: http://localhost:8501")
        print("3. Explore as visualizações disponíveis")
        print("\n⏹️  Para parar o dashboard, pressione Ctrl+C")
        
        # Aguarda o processo
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Dashboard interrompido pelo usuário")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"❌ Erro ao iniciar dashboard: {e}")

def show_quick_stats():
    """Mostra estatísticas rápidas do banco"""
    print("\n📊 Estatísticas Rápidas do Banco de Dados:")
    
    try:
        import psycopg2
        
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="database_trabalho",
            user="postgres",
            password="admin"
        )
        
        cursor = conn.cursor()
        
        # Total de registros
        cursor.execute("SELECT COUNT(*) FROM temperature_readings")
        total = cursor.fetchone()[0]
        print(f"   📈 Total de registros: {total:,}")
        
        # Dispositivos únicos
        cursor.execute("SELECT COUNT(DISTINCT room_id) FROM temperature_readings")
        devices = cursor.fetchone()[0]
        print(f"   🏠 Dispositivos únicos: {devices}")
        
        # Range de datas
        cursor.execute("""
            SELECT 
                MIN(noted_date) as min_date,
                MAX(noted_date) as max_date,
                ROUND(AVG(temperature), 2) as avg_temp
            FROM temperature_readings
        """)
        stats = cursor.fetchone()
        print(f"   📅 Período: {stats[0]} até {stats[1]}")
        print(f"   🌡️  Temperatura média: {stats[2]}°C")
        
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Erro ao conectar com o banco: {e}")

def main():
    """Função principal"""
    print_banner()
    
    # Verifica requisitos
    if not check_requirements():
        print("\n❌ Requisitos não atendidos. Verifique as dependências.")
        sys.exit(1)
    
    # Menu de opções
    print("\n📋 Opções disponíveis:")
    print("1. 🏃 Executar pipeline completo (processamento + dashboard)")
    print("2. 📊 Apenas processar dados")
    print("3. 🚀 Apenas iniciar dashboard")
    print("4. 📈 Mostrar estatísticas do banco")
    print("5. ❌ Sair")
    
    while True:
        try:
            choice = input("\n🎯 Escolha uma opção (1-5): ").strip()
            
            if choice == "1":
                # Pipeline completo
                if run_data_processing():
                    show_quick_stats()
                    start_dashboard()
                break
                
            elif choice == "2":
                # Apenas processamento
                if run_data_processing():
                    show_quick_stats()
                break
                
            elif choice == "3":
                # Apenas dashboard
                start_dashboard()
                break
                
            elif choice == "4":
                # Estatísticas
                show_quick_stats()
                continue
                
            elif choice == "5":
                # Sair
                print("👋 Até logo!")
                break
                
            else:
                print("❌ Opção inválida. Escolha entre 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Operação cancelada pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            break

if __name__ == "__main__":
    main()
