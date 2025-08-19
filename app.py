import pandas as pd
import streamlit as st
import plotly.express as px

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Dashboard de Não Conformidades",
    page_icon="📊",
    layout="wide",
)

# --- Carregamento dos dados ---
url = ''
#df = pd.read_excel(r"C:\Users\Magno\OneDrive\Personal\Caio\Checklist das pendencias.xlsx", sheet_name='preparada')
df['Desc_gravidade'] = df['Gravidade'].apply(lambda x: 'Baixa' if x == 1 else ('Media' if x == 2 else ('Alta' if x == 3 else 'erro')))
#print(df.head())

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Local
locais_disponiveis = sorted(df['Local'].unique())
locais_disponiveis_selecionados = st.sidebar.multiselect("Local", 
                                                         locais_disponiveis, 
                                                         default=locais_disponiveis)

# filtro de gravidade
gravidade = sorted(df['Desc_gravidade'].unique())
gravidade_selecionados = st.sidebar.multiselect("Gravidade", 
                                               gravidade, 
                                               default=gravidade)

# filtro de responsável
responsavel = sorted(df['Responsável'].unique())
responsavel_selecionados = st.sidebar.multiselect("Responsavel", 
                                               responsavel, 
                                               default=responsavel)

# filtro de elevador
equipamento = sorted(df['Elevador_ Local'].unique())
equipamento_selecionados = st.sidebar.multiselect("Equipamento", 
                                               equipamento, 
                                               default=equipamento)


# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[
    (df['Local'].isin(locais_disponiveis_selecionados)) &
    (df['Desc_gravidade'].isin(gravidade_selecionados)) &
    (df['Elevador_ Local'].isin(equipamento_selecionados)) &
    (df['Responsável'].isin(responsavel_selecionados))    
]

# --- Conteúdo Principal ---
st.title("🎲 Dashboard de Não Conformidades - Manutenção de elevadores")
st.markdown("Explore as informações do levantamento realizado. Utilize os filtros à esquerda para refinar sua análise.")

# --- Métricas Principais (KPIs) ---
st.subheader("Métricas gerais dos dados obtidos")

if not df_filtrado.empty:
    nconformidades = df_filtrado.shape[0]
    alta = (df_filtrado['Desc_gravidade'] == 'Alta').sum()
    media = (df_filtrado['Desc_gravidade'] == 'Media').sum()
    baixa = (df_filtrado['Desc_gravidade'] == 'Baixa').sum()
else:
    nconformidades, alta, media, baixa = 0, 0, 0, 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Não Conformidades", f"{nconformidades:,.0f}")
col2.metric("Gravidade Alta", f"{alta:,.0f}")
col3.metric("Gravidade Média", f"{media:,}")
col4.metric("Gravidade Baixa", f"{baixa:,}")

st.markdown("---")

# --- Análises Visuais com Plotly ---
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        gravidade_percentual = df['Desc_gravidade'].value_counts(normalize=True).reset_index()
        gravidade_percentual.columns = ['Desc_gravidade', 'Percentage']

        color_map = {
        'Alta': '#B22222',   # Vermelho mais fechado
        'Media': '#FFD580',  # Laranja pastel claro
        'Baixa': '#98FB98'   # Verde suave
    }

        pie_percentual = px.pie(
            gravidade_percentual,
            values='Percentage',
            names='Desc_gravidade',
            color='Desc_gravidade',
            color_discrete_map=color_map,
            hole=0.4
        )

        pie_percentual.update_layout(
            width=700,
            height=500,
            title={'text' : 'Percentual de casos por Gravidade',
                'y': 0.95,
                'x': 0.5,
                'font': {'weight': 'bold'}},
            legend=dict(
                orientation="h",   # horizontal
                yanchor="top",
                y=-0.2,            # posição abaixo
                xanchor="center",
                x=0.5              # centraliza
            )
        )
        st.plotly_chart(pie_percentual, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de não conformidades percentual.")

with col_graf2:
    if not df_filtrado.empty:
        responsavel_counts = df['Responsável'].value_counts().reset_index()
        responsavel_counts.columns = ['Responsável', 'Quantidade']

        responsavel_bar = px.bar(responsavel_counts,
                    x='Responsável',
                    y='Quantidade',
                    color_discrete_map=color_map,
                    template='plotly_white'
                    )

        responsavel_bar.update_layout(width=700, height=500,
                        xaxis_title= 'Responsável',
                        yaxis_title= 'Quantidade',
                        showlegend=False,
                        title={'text' : 'Quantidade de Casos por Responsável',
                                'y': 0.92,
                                'x': 0.5,
                                'font': {'weight': 'bold'}}
                        ) 
        st.plotly_chart(responsavel_bar, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de responsabilidade.")

# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")

st.dataframe(df_filtrado)
