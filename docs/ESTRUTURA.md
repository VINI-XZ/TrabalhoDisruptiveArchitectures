# 📁 Estrutura Organizada do Projeto IoT

## 🎯 Visão Geral

O projeto foi reorganizado em uma estrutura de pastas profissional e lógica, facilitando a manutenção, desenvolvimento e colaboração.

## 📂 Estrutura de Pastas

```
📁 Projeto IoT/
├── 📁 src/                    # Código fonte Python
│   ├── __init__.py           # Inicialização do pacote
│   ├── iot_data_processor.py # Processador de dados IoT
│   └── dashboard.py          # Dashboard Streamlit
├── 📁 data/                   # Dados e arquivos CSV
│   └── IOT-temp.csv         # Dataset de temperaturas
├── 📁 config/                 # Configurações e scripts SQL
│   ├── config.py            # Configurações centralizadas
│   └── init.sql             # Script de inicialização do banco
├── 📁 docs/                   # Documentação
│   ├── README.md            # Documentação detalhada
│   ├── EXECUTAR.md          # Guia de execução
│   └── ESTRUTURA.md         # Este arquivo
├── 📁 scripts/                # Scripts de execução
│   ├── run_pipeline.py      # Script de execução automatizada
│   └── start.py             # Script de inicialização melhorado
├── 📁 logs/                   # Arquivos de log
│   └── iot_pipeline.log     # Logs do processamento
├── 📄 .gitignore             # Arquivos ignorados pelo Git
├── 📄 docker-compose.yml     # Configuração Docker Compose
├── 📄 Dockerfile            # Configuração Docker
├── 📄 requirements.txt      # Dependências Python
├── 📄 setup.py             # Configuração do pacote
└── 📄 README.md            # Documentação principal
```

## 🔧 Melhorias Implementadas

### 1. **Separação de Responsabilidades**
- **`src/`**: Todo o código Python em um local centralizado
- **`data/`**: Dados e arquivos CSV separados do código
- **`config/`**: Configurações e scripts SQL organizados
- **`docs/`**: Documentação centralizada
- **`scripts/`**: Scripts de execução e automação
- **`logs/`**: Logs separados para facilitar monitoramento

### 2. **Configuração Centralizada**
- **`config/config.py`**: Todas as configurações em um local
- Variáveis de ambiente suportadas
- Caminhos dinâmicos baseados no contexto
- Configurações de banco, Streamlit e processamento

### 3. **Scripts Melhorados**
- **`scripts/start.py`**: Script de inicialização com menu interativo
- Verificação automática da estrutura
- Suporte a execução local e Docker
- Validação de dependências

### 4. **Compatibilidade Docker**
- Caminhos atualizados no `docker-compose.yml`
- Suporte a execução local e containerizada
- Volumes mapeados corretamente

### 5. **Documentação Aprimorada**
- README principal na raiz
- Documentação detalhada em `docs/`
- Guias de execução específicos
- Estrutura clara e navegável

## 🚀 Como Executar

### Método 1: Script de Inicialização (Recomendado)
```bash
py scripts/start.py
```

### Método 2: Execução Manual
```bash
# Processar dados
py src/iot_data_processor.py

# Iniciar dashboard
py -m streamlit run src/dashboard.py
```

### Método 3: Docker Compose
```bash
docker-compose up -d
```

## 📋 Benefícios da Nova Estrutura

### ✅ **Organização**
- Código separado por função
- Fácil localização de arquivos
- Estrutura profissional

### ✅ **Manutenibilidade**
- Configurações centralizadas
- Código modular
- Fácil atualização

### ✅ **Escalabilidade**
- Estrutura preparada para crescimento
- Fácil adição de novos módulos
- Separação clara de responsabilidades

### ✅ **Colaboração**
- Estrutura padrão da indústria
- Fácil onboarding de novos desenvolvedores
- Documentação clara

### ✅ **Deploy**
- Suporte completo ao Docker
- Configurações de ambiente
- Scripts de automação

## 🔄 Migração de Código Existente

### Arquivos Movidos
- `iot_data_processor.py` → `src/iot_data_processor.py`
- `dashboard.py` → `src/dashboard.py`
- `run_pipeline.py` → `scripts/run_pipeline.py`
- `IOT-temp.csv` → `data/IOT-temp.csv`
- `init.sql` → `config/init.sql`
- `README.md` → `docs/README.md`
- `EXECUTAR.md` → `docs/EXECUTAR.md`

### Caminhos Atualizados
- Referências de arquivos CSV atualizadas
- Caminhos de log corrigidos
- Imports e dependências ajustados
- Configurações Docker atualizadas

## 🎯 Próximos Passos

1. **Testar a nova estrutura** com os scripts fornecidos
2. **Verificar compatibilidade** com o ambiente existente
3. **Atualizar documentação** conforme necessário
4. **Implementar melhorias** baseadas no feedback

## 📞 Suporte

Para dúvidas sobre a nova estrutura:
- Consulte a documentação em `docs/`
- Verifique os logs em `logs/`
- Execute `py scripts/start.py` para diagnóstico automático

---

**Estrutura organizada por**: VINI-XZ  
**Data**: 18/09/2025  
**Versão**: 1.0.0
