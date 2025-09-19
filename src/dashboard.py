#!/usr/bin/env python3
"""
Dashboard IoT - Visualização de Dados de Temperatura
Dashboard interativo para análise de dados de temperatura de dispositivos IoT
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine, text
import logging
from datetime import datetime, timedelta
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Dashboard IoT - Temperaturas",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração de logging
logging.basicConfig(level=logging.INFO)

class IoTDashboard:
    def __init__(self):
        """Inicializa o dashboard IoT"""
        self.engine = None
        self.db_config = {
            'host': 'localhost',
            'port': '5432',
            'database': 'database_trabalho',
            'user': 'postgres',
            'password': 'admin'
        }
        
    def connect_database(self):
        """Estabelece conexão com o PostgreSQL"""
        try:
            connection_string = (
                f"postgresql://{self.db_config['user']}:{self.db_config['password']}"
                f"@{self.db_config['host']}:{self.db_config['port']}"
                f"/{self.db_config['database']}"
            )
            
            self.engine = create_engine(connection_string)
            
            # Testa a conexão
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                return True
                
        except Exception as e:
            st.error(f"❌ Erro ao conectar com PostgreSQL: {e}")
            return False
    
    def load_data(self, query):
        """Carrega dados do banco usando uma query SQL"""
        try:
            with self.engine.connect() as conn:
                return pd.read_sql(query, conn)
        except Exception as e:
            st.error(f"❌ Erro ao carregar dados: {e}")
            return pd.DataFrame()
    
    def load_view_data(self, view_name):
        """Carrega dados de uma view específica"""
        return self.load_data(f"SELECT * FROM {view_name}")
    
    def get_database_stats(self):
        """Obtém estatísticas gerais do banco"""
        stats_query = """
        SELECT 
            COUNT(*) as total_readings,
            COUNT(DISTINCT room_id) as total_devices,
            MIN(noted_date) as earliest_date,
            MAX(noted_date) as latest_date,
            ROUND(AVG(temperature), 2) as avg_temperature,
            ROUND(MIN(temperature), 2) as min_temperature,
            ROUND(MAX(temperature), 2) as max_temperature
        FROM temperature_readings
        """
        return self.load_data(stats_query)
    
    def create_temperature_distribution_chart(self):
        """Cria gráfico de distribuição de temperaturas"""
        query = """
        SELECT 
            temp_range,
            count
        FROM (
            SELECT 
                CASE 
                    WHEN temperature < 20 THEN 'Muito Frio (<20°C)'
                    WHEN temperature BETWEEN 20 AND 25 THEN 'Frio (20-25°C)'
                    WHEN temperature BETWEEN 25 AND 30 THEN 'Normal (25-30°C)'
                    WHEN temperature BETWEEN 30 AND 35 THEN 'Quente (30-35°C)'
                    ELSE 'Muito Quente (>35°C)'
                END as temp_range,
                COUNT(*) as count,
                CASE 
                    WHEN temperature < 20 THEN 1
                    WHEN temperature BETWEEN 20 AND 25 THEN 2
                    WHEN temperature BETWEEN 25 AND 30 THEN 3
                    WHEN temperature BETWEEN 30 AND 35 THEN 4
                    ELSE 5
                END as sort_order
            FROM temperature_readings
            GROUP BY 
                CASE 
                    WHEN temperature < 20 THEN 'Muito Frio (<20°C)'
                    WHEN temperature BETWEEN 20 AND 25 THEN 'Frio (20-25°C)'
                    WHEN temperature BETWEEN 25 AND 30 THEN 'Normal (25-30°C)'
                    WHEN temperature BETWEEN 30 AND 35 THEN 'Quente (30-35°C)'
                    ELSE 'Muito Quente (>35°C)'
                END,
                CASE 
                    WHEN temperature < 20 THEN 1
                    WHEN temperature BETWEEN 20 AND 25 THEN 2
                    WHEN temperature BETWEEN 25 AND 30 THEN 3
                    WHEN temperature BETWEEN 30 AND 35 THEN 4
                    ELSE 5
                END
        ) as temp_data
        ORDER BY sort_order
        """
        
        df = self.load_data(query)
        
        if not df.empty:
            fig = px.pie(
                df, 
                values='count', 
                names='temp_range',
                title="Distribuição de Leituras por Faixa de Temperatura",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            return fig
        return None
    
    def create_device_comparison_chart(self):
        """Cria gráfico de comparação entre dispositivos"""
        df = self.load_view_data('avg_temp_por_dispositivo')
        
        if not df.empty:
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Temperatura Média por Dispositivo', 'Número de Leituras por Dispositivo'),
                vertical_spacing=0.1
            )
            
            # Gráfico de temperatura média
            fig.add_trace(
                go.Bar(
                    x=df['device_id'],
                    y=df['avg_temp'],
                    name='Temperatura Média',
                    marker_color='lightblue'
                ),
                row=1, col=1
            )
            
            # Gráfico de número de leituras
            fig.add_trace(
                go.Bar(
                    x=df['device_id'],
                    y=df['total_readings'],
                    name='Total de Leituras',
                    marker_color='lightcoral'
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                height=600,
                showlegend=False,
                title_text="Análise Comparativa dos Dispositivos"
            )
            
            fig.update_xaxes(title_text="Dispositivo", row=2, col=1)
            fig.update_yaxes(title_text="Temperatura (°C)", row=1, col=1)
            fig.update_yaxes(title_text="Número de Leituras", row=2, col=1)
            
            return fig
        return None
    
    def create_temporal_analysis_chart(self):
        """Cria análise temporal das temperaturas"""
        df = self.load_view_data('leituras_por_hora')
        
        if not df.empty:
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Leituras por Hora do Dia', 'Temperatura Média por Hora'),
                vertical_spacing=0.1
            )
            
            # Leituras por hora
            fig.add_trace(
                go.Scatter(
                    x=df['hora'],
                    y=df['contagem'],
                    mode='lines+markers',
                    name='Leituras por Hora',
                    line=dict(color='blue', width=3),
                    marker=dict(size=8)
                ),
                row=1, col=1
            )
            
            # Temperatura média por hora
            fig.add_trace(
                go.Scatter(
                    x=df['hora'],
                    y=df['temp_media'],
                    mode='lines+markers',
                    name='Temperatura Média',
                    line=dict(color='red', width=3),
                    marker=dict(size=8)
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                height=600,
                showlegend=False,
                title_text="Análise Temporal - Padrões por Hora"
            )
            
            fig.update_xaxes(title_text="Hora do Dia", row=2, col=1)
            fig.update_yaxes(title_text="Número de Leituras", row=1, col=1)
            fig.update_yaxes(title_text="Temperatura (°C)", row=2, col=1)
            
            return fig
        return None
    
    def create_daily_temperature_chart(self):
        """Cria gráfico de temperaturas por dia"""
        df = self.load_view_data('temp_max_min_por_dia')
        
        if not df.empty:
            # Limita aos últimos 30 dias para melhor visualização
            df['data'] = pd.to_datetime(df['data'])
            df = df.sort_values('data').tail(30)
            
            fig = go.Figure()
            
            # Linha de temperatura máxima
            fig.add_trace(go.Scatter(
                x=df['data'],
                y=df['temp_max'],
                mode='lines+markers',
                name='Temperatura Máxima',
                line=dict(color='red', width=2),
                marker=dict(size=6)
            ))
            
            # Linha de temperatura média
            fig.add_trace(go.Scatter(
                x=df['data'],
                y=df['temp_media'],
                mode='lines+markers',
                name='Temperatura Média',
                line=dict(color='blue', width=2),
                marker=dict(size=6)
            ))
            
            # Linha de temperatura mínima
            fig.add_trace(go.Scatter(
                x=df['data'],
                y=df['temp_min'],
                mode='lines+markers',
                name='Temperatura Mínima',
                line=dict(color='green', width=2),
                marker=dict(size=6)
            ))
            
            fig.update_layout(
                title="Temperaturas por Dia (Últimos 30 dias)",
                xaxis_title="Data",
                yaxis_title="Temperatura (°C)",
                height=500,
                hovermode='x unified'
            )
            
            return fig
        return None
    
    def create_location_analysis_chart(self):
        """Cria análise por tipo de localização"""
        df = self.load_view_data('analise_por_tipo_localizacao')
        
        if not df.empty:
            fig = px.bar(
                df,
                x='location_type',
                y=['temp_media', 'temp_max', 'temp_min'],
                title="Análise de Temperatura por Tipo de Localização",
                labels={'value': 'Temperatura (°C)', 'variable': 'Tipo de Medição'},
                color_discrete_map={
                    'temp_media': 'blue',
                    'temp_max': 'red',
                    'temp_min': 'green'
                }
            )
            
            fig.update_layout(
                height=500,
                xaxis_title="Tipo de Localização",
                yaxis_title="Temperatura (°C)"
            )
            
            return fig
        return None
    
    def create_extreme_temperatures_table(self):
        """Cria tabela com temperaturas extremas"""
        df = self.load_view_data('top_10_temperaturas_altas')
        
        if not df.empty:
            # Formata a data
            df['noted_date'] = pd.to_datetime(df['noted_date']).dt.strftime('%d/%m/%Y %H:%M')
            
            return df
        return pd.DataFrame()
    
    def run_dashboard(self):
        """Executa o dashboard principal"""
        # Conecta ao banco
        if not self.connect_database():
            st.stop()
        
        # Título principal
        st.title("🌡️ Dashboard IoT - Análise de Temperaturas")
        st.markdown("---")
        
        # Sidebar com informações do banco
        with st.sidebar:
            st.header("📊 Estatísticas do Banco")
            
            stats = self.get_database_stats()
            if not stats.empty:
                stat = stats.iloc[0]
                
                st.metric("Total de Leituras", f"{stat['total_readings']:,}")
                st.metric("Dispositivos", stat['total_devices'])
                st.metric("Temperatura Média", f"{stat['avg_temperature']}°C")
                st.metric("Temperatura Mínima", f"{stat['min_temperature']}°C")
                st.metric("Temperatura Máxima", f"{stat['max_temperature']}°C")
                
                st.markdown("---")
                st.markdown(f"**Período dos Dados:**")
                st.markdown(f"• Início: {stat['earliest_date'].strftime('%d/%m/%Y')}")
                st.markdown(f"• Fim: {stat['latest_date'].strftime('%d/%m/%Y')}")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📈 Total de Leituras",
                f"{stats.iloc[0]['total_readings']:,}" if not stats.empty else "0"
            )
        
        with col2:
            st.metric(
                "🏠 Dispositivos",
                stats.iloc[0]['total_devices'] if not stats.empty else "0"
            )
        
        with col3:
            st.metric(
                "🌡️ Temp. Média",
                f"{stats.iloc[0]['avg_temperature']}°C" if not stats.empty else "0°C"
            )
        
        with col4:
            temp_range = stats.iloc[0]['max_temperature'] - stats.iloc[0]['min_temperature']
            st.metric(
                "📊 Amplitude",
                f"{temp_range:.1f}°C" if not stats.empty else "0°C"
            )
        
        st.markdown("---")
        
        # Gráficos principais
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Visão Geral", 
            "🏠 Dispositivos", 
            "⏰ Análise Temporal", 
            "📅 Por Dia", 
            "📍 Por Localização"
        ])
        
        with tab1:
            st.header("Distribuição de Temperaturas")
            fig_dist = self.create_temperature_distribution_chart()
            if fig_dist:
                st.plotly_chart(fig_dist, width='stretch')
            
            st.header("Top 10 Temperaturas Mais Altas")
            extreme_df = self.create_extreme_temperatures_table()
            if not extreme_df.empty:
                st.dataframe(
                    extreme_df,
                    width='stretch',
                    hide_index=True
                )
        
        with tab2:
            st.header("Análise Comparativa dos Dispositivos")
            fig_devices = self.create_device_comparison_chart()
            if fig_devices:
                st.plotly_chart(fig_devices, width='stretch')
        
        with tab3:
            st.header("Análise Temporal - Padrões por Hora")
            fig_temporal = self.create_temporal_analysis_chart()
            if fig_temporal:
                st.plotly_chart(fig_temporal, width='stretch')
        
        with tab4:
            st.header("Evolução das Temperaturas por Dia")
            fig_daily = self.create_daily_temperature_chart()
            if fig_daily:
                st.plotly_chart(fig_daily, width='stretch')
        
        with tab5:
            st.header("Análise por Tipo de Localização")
            fig_location = self.create_location_analysis_chart()
            if fig_location:
                st.plotly_chart(fig_location, width='stretch')
        
        # Rodapé
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: #666;'>
                Dashboard IoT - Análise de Dados de Temperatura<br>
                Desenvolvido com Streamlit e Plotly
            </div>
            """,
            unsafe_allow_html=True
        )

def main():
    """Função principal"""
    dashboard = IoTDashboard()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main()
