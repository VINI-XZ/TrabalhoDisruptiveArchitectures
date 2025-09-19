#!/usr/bin/env python3
"""
Script de Setup - Pipeline de Dados IoT
Este script automatiza a configuração e execução do pipeline completo
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def run_command(command, description):
    """Executa um comando e mostra o progresso"""
    print(f"\n🔄 {description}")
    print(f"Comando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Sucesso!")
        if result.stdout:
            print(f"Saída: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erro!")
        print(f"Erro: {e.stderr}")
        return False

def check_docker():
    """Verifica se o Docker está instalado e rodando"""
    print("🔍 Verificando Docker...")
    
    # Verifica se o Docker está instalado
    if not run_command("docker --version", "Verificando instalação do Docker"):
        print("❌ Docker não está instalado. Instale o Docker primeiro.")
        return False
    
    # Verifica se o Docker está rodando
    if not run_command("docker info", "Verificando se Docker está rodando"):
        print("❌ Docker não está rodando. Inicie o Docker primeiro.")
        return False
    
    print("✅ Docker está funcionando corretamente!")
    return True

def check_python_packages():
    """Verifica se os pacotes Python necessários estão instalados"""
    print("🔍 Verificando pacotes Python...")
    
    required_packages = [
        'pandas',
        'psycopg2-binary',
        'sqlalchemy',
        'streamlit',
        'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} - Instalado")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Não instalado")
    
    if missing_packages:
        print(f"\n📦 Instalando pacotes faltantes: {', '.join(missing_packages)}")
        install_command = f"pip install {' '.join(missing_packages)}"
        return run_command(install_command, "Instalando pacotes Python")
    
    return True

def setup_docker_environment():
    """Configura o ambiente Docker"""
    print("🐳 Configurando ambiente Docker...")
    
    # Para containers existentes
    run_command("docker stop postgres-iot iot-dashboard 2>/dev/null || true", "Parando containers existentes")
    run_command("docker rm postgres-iot iot-dashboard 2>/dev/null || true", "Removendo containers existentes")
    
    # Constrói e inicia os containers
    if run_command("docker-compose up -d postgres-iot", "Iniciando PostgreSQL"):
        print("⏳ Aguardando PostgreSQL inicializar...")
        time.sleep(10)  # Aguarda o PostgreSQL inicializar
        
        if run_command("docker-compose up -d", "Iniciando todos os serviços"):
            return True
    
    return False

def run_data_pipeline():
    """Executa o pipeline de dados"""
    print("📊 Executando pipeline de dados...")
    
    # Verifica se o arquivo CSV existe
    csv_file = "IOT-temp.csv"
    if not Path(csv_file).exists():
        print(f"❌ Arquivo {csv_file} não encontrado!")
        return False
    
    # Executa o script de processamento
    return run_command("python iot_data_processor.py", "Processando dados IoT")

def show_status():
    """Mostra o status dos serviços"""
    print("\n📊 Status dos Serviços:")
    print("=" * 50)
    
    # Status do PostgreSQL
    postgres_status = subprocess.run(
        "docker exec postgres-iot pg_isready -U postgres -d database_trabalho",
        shell=True, capture_output=True
    )
    
    if postgres_status.returncode == 0:
        print("✅ PostgreSQL: Rodando")
        print("   📍 Host: localhost:5432")
        print("   🗄️  Banco: database_trabalho")
        print("   👤 Usuário: postgres")
        print("   🔑 Senha: admin")
    else:
        print("❌ PostgreSQL: Não disponível")
    
    # Status do Dashboard
    dashboard_status = subprocess.run(
        "curl -s http://localhost:8501 > /dev/null",
        shell=True, capture_output=True
    )
    
    if dashboard_status.returncode == 0:
        print("✅ Dashboard: Rodando")
        print("   🌐 URL: http://localhost:8501")
    else:
        print("❌ Dashboard: Não disponível")
    
    print("\n📋 Próximos Passos:")
    print("1. Execute: python iot_data_processor.py")
    print("2. Acesse: http://localhost:8501")
    print("3. Para parar: docker-compose down")

def main():
    """Função principal do setup"""
    print("🚀 Setup do Pipeline de Dados IoT")
    print("=" * 50)
    
    # Verifica pré-requisitos
    if not check_docker():
        sys.exit(1)
    
    if not check_python_packages():
        sys.exit(1)
    
    # Configura ambiente Docker
    if not setup_docker_environment():
        print("❌ Erro ao configurar ambiente Docker")
        sys.exit(1)
    
    # Mostra status
    show_status()
    
    print("\n🎉 Setup concluído com sucesso!")
    print("\nPara executar o pipeline de dados:")
    print("python iot_data_processor.py")
    print("\nPara acessar o dashboard:")
    print("http://localhost:8501")

if __name__ == "__main__":
    main()
