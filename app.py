import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="BanVic Dashboard", 
    page_icon="🪙",
    layout="wide")

# Carregando os dados
df = pd.read_csv("df_tb1_completa.csv")
df2 = pd.read_csv("df_tb2_completa.csv")

#inicio do dashboard
st.title("Dashboard BanVic")

#Colunas de métricas KPIs
col1, col2, col3 = st.columns(3)
#Numero total de Clientes
with col1:
    num_clientes_unicos = df['cod_cliente'].nunique()
    st.metric("Total de Clientes Únicos", f"{num_clientes_unicos:,}")
#Volume total do banco
with col2:
    volume_total = df['valor_transacao'].sum()
    st.metric("Volume Total do Banco", f"R$ {volume_total:,.2f}")
#Taxa de aprovação de propostas
with col3:
    num_propostas_aprovadas = df2[df2['status_proposta'] == 'Aprovada']['cod_proposta'].nunique()
    num_propostas_totais = df2['cod_proposta'].nunique()
    taxa_aprovacao = (num_propostas_aprovadas / num_propostas_totais) * 100
    st.metric("Taxa de Aprovação de Propostas", f"{taxa_aprovacao:.2f}%")

#Colunas de graficos
c1, c2 = st.columns(2)
#Grafico de Barra - Ranking de Agencias por Volume de Transações
with c1:
    st.subheader("Ranking de Agências por Volume de Transações")
    agencia_volume = df.groupby('cod_agencia')['valor_transacao'].sum().reset_index()
    agencia_volume = agencia_volume.sort_values(by='valor_transacao', ascending=False).head(10)
    fig1 = px.bar(agencia_volume, x='cod_agencia', y='valor_transacao',
              labels={'cod_agencia': 'Código da Agência', 'valor_transacao': 'Volume de Transações'},
              title='Top 10 Agências por Volume de Transações')
    st.plotly_chart(fig1, use_container_width=True)

#Grafico de Pizza - Clientes Pf vs Pj
with c2:
    st.subheader("Distribuição de Clientes PF vs PJ")
    cliente_tipo = df[['cod_cliente', 'tipo_cliente']].drop_duplicates()
    cliente_tipo_count = cliente_tipo['tipo_cliente'].value_counts().reset_index()
    cliente_tipo_count.columns = ['tipo_cliente', 'count']
    fig2 = px.pie(cliente_tipo_count, names='tipo_cliente', values='count',
              title='Distribuição de Clientes PF vs PJ')
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
#Grafico de Pizza - Distribução de Tipo de Transação
with c3:
    st.subheader("Distribuição de Tipo de Transação")
    tipos_transacao = df['nome_transacao'].value_counts().reset_index()
    tipos_transacao.columns = ['tipo_transacao', 'quantidade']
    fig3 = px.pie(tipos_transacao, 
                  names='tipo_transacao', 
                  values='quantidade',
              title='Tipos de Transações Realizadas')
    st.plotly_chart(fig3, use_container_width=True)