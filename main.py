import streamlit as st
import pickle
from datetime import date
import pandas as pd
import altair as alt
import plotly.express as px

st.title("MPCEC BR - Modelo Preditivo de Consumo Elétrico Coletivo Brasileiro")

#Código

# Carregar o modelo
with open('modelo.pkl', 'rb') as file:
    model = pickle.load(file)

mapeamento_estado = {
    'Roraima': 1,
    'Acre': 2,
    'Amazonas': 3,
    'Rondônia': 4,
    'Pará': 5,
    'Amapá': 6,
    'Tocantins': 7,
    'Maranhão': 8,
    'Piauí': 9,
    'Ceará': 10,
    'Rio Grande do Norte': 11,
    'Paraíba': 12,
    'Pernambuco': 13,
    'Alagoas': 14,
    'Sergipe': 15,
    'Bahia': 16,
    'Minas Gerais': 17,
    'Espírito Santo': 18,
    'Rio de Janeiro': 19,
    'São Paulo': 20,
    'Paraná': 21,
    'Santa Catarina': 22,
    'Rio Grande do Sul': 23,
    'Mato Grosso do Sul': 24,
    'Mato Grosso': 25,
    'Goiás': 26,
    'Distrito Federal': 27
}

# Definir dicionário de mapeamento para tipo de consumo
mapeamento_consumo = {
    'Total': 1, 'Cativo': 2, 'Residencial': 3, 'Industrial': 4, 'Comercial': 5, 'Outros': 6
}

ano_intervalo = st.slider("Selecione o intervalo de anos para fazer a previsão", 2004, 2050, (2020, 2030))
estado = st.selectbox('Agora o estado em que deseja tentar prever o consumo', list(mapeamento_estado.keys()))

consumo_num = st.selectbox('E então, qual o tipo de consumo que será previsto?', list(mapeamento_consumo.keys()))
numero_consumidores = st.number_input('Numero de consumidores', value=1)
mes = st.selectbox('E qual o mês de consumo?', range(1, 13))

# Mapear valores selecionados para valores numéricos
sigla_uf = mapeamento_estado[estado]
tipo_consumo = mapeamento_consumo[consumo_num]

# Usar o modelo para fazer previsões
previsoes = []
for ano in range(ano_intervalo[0], ano_intervalo[1] + 1):
    input_data = [[ano, mes, sigla_uf, tipo_consumo, numero_consumidores]]
    prediction = model.predict(input_data)
    previsoes.append({"Ano": ano, "Mês": mes, "Previsão de Consumo": prediction[0]})

# Exibir o resultado da previsão
st.write('### Previsão de consumo para o estado de ' + str(estado) + ' no intervalo de anos ' + str(ano_intervalo[0]) + ' a ' + str(ano_intervalo[1]) + ' com número de consumidores de ' + str(numero_consumidores) + ' e o tipo de consumo ' + str(consumo_num) + ' em MWh:')
df = pd.DataFrame(previsoes)
chart = alt.Chart(df).mark_bar().encode(
    x="Ano",
    y="Previsão de Consumo",
    color="Mês"
).properties(
    width=800,
    height=400,
    title="Previsão de Consumo Elétrico"
)
st.altair_chart(chart, use_container_width=True)
