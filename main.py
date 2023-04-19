import streamlit as st
import pickle
from datetime import date
import matplotlib.pyplot as plt

st.title("MPCEC BR - Modelo Preditivo de Consumo Elétrico Coletivo Brasileiro")

st.write(""" 
Aqui mostramos uma análise preditiva dos dados com base em um conjunto de dados contendo dados de consumo elétrico do Brasil por estado, mes e ano, tipo de consumo e quantidade de consumidores
este modelo foi treinado usando um algoritmo de regressão linear para tentar prever o consumo usando as variávies citadas.
""")

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

ano_mes = st.date_input('Selecione o ano e mês', min_value=date(2004, 1, 1), max_value=date(2050, 12, 31))
estado = st.selectbox('Estado do Brasil', list(mapeamento_estado.keys()))
consumo_num = st.selectbox('Tipo de consumo', list(mapeamento_consumo.keys()))
numero_consumidores = st.number_input('Número de consumidores', value=1)

# Mapear valores selecionados para valores numéricos
sigla_uf = mapeamento_estado[estado]
tipo_consumo = mapeamento_consumo[consumo_num]

# Usar o modelo para fazer previsões
ano = ano_mes.year
mes = ano_mes.month
input_data = [[ano, mes, sigla_uf, tipo_consumo, numero_consumidores]]
prediction = model.predict(input_data)

# Exibir o resultado da previsão
st.write('A previsão é:', prediction)

# Plotar gráfico interativo
import pandas as pd
import altair as alt

# Criar DataFrame com os dados de entrada
df_input = pd.DataFrame({
    'Ano': [ano],
    'Mês': [mes],
    'Estado': [sigla_uf],
    'Tipo de Consumo': [tipo_consumo],
    'Número de Consumidores': [numero_consumidores]
})

# Plotar gráfico de barras com o valor previsto
df_output = pd.DataFrame({'Valor Previsto': [prediction[0]]})
bars = alt.Chart(df_output).mark_bar().encode(y='Valor Previsto')
text = bars.mark_text(
    align='center',
    baseline='bottom',
    dy=-10
).encode(text='Valor Previsto')
chart = (bars + text).properties(title='Valor previsto pelo modelo')

# Plotar gráfico de dispersão com os valores de entrada
scatter = alt.Chart(df_input).mark_point(size=100, opacity=0.7, color='red').encode(
    x='Ano:O',
    y='Número de Consumidores:Q',
    tooltip=['Ano', 'Mês', 'Estado', 'Tipo de Consumo', 'Número de Consumidores']
).properties(title='Valores de entrada')

# Combinar os dois gráficos em um único gráfico interativo
st.altair_chart(chart + scatter, use_container_width=True)

# GRAFICOS

# Usar o modelo para fazer previsões para os próximos 12 meses
input_data = [[ano, mes, sigla_uf, tipo_consumo, numero_consumidores]]
df_predictions = pd.DataFrame(columns=['Data', 'Previsão'])
for i in range(12):
    mes += 1
    if mes > 12:
        ano += 1
        mes = 1
    input_data[0][0] = ano
    input_data[0][1] = mes
    prediction = model.predict(input_data)[0]
    df_predictions.loc[i] = [date(ano, mes, 1), prediction]

# Plotar gráfico de linha com as previsões
line_chart = alt.Chart(df_predictions).mark_line().encode(
    x='Data:T',
    y='Previsão:Q',
    tooltip=['Data', 'Previsão']
).properties(title='Previsão para os próximos 12 meses')

# Mostrar gráficos na página
st.altair_chart(chart + scatter + line_chart, use_container_width=True)

st.write(""" 
Agora vamos para parte mais exploatória dos dados mostrando o conjunto de dados bruto que foi usado para gerar este modelo com alguns gráficos:
""")

df = pd.read_csv("novos_dados.csv")

#st.dataframe(df.head(10))

st.write(""" 
### Consumo coletivo ao longo dos anos:
como pode ver existe uma divisão de temperatura por meses, com janeiro sendo 1 e indo até dezembro que é 12
""")

# Convertendo a coluna 'ano' para o tipo de dados de data
df['ano'] = pd.to_datetime(df['ano'], format='%Y')


st.write(""" 
### Grafico de dispersão
""")

# Criando um gráfico interativo de dispersão com Altair
scatter_chart = alt.Chart(df).mark_circle().encode(
    x=alt.X('ano:T', axis=alt.Axis(format='%Y')),
    y='consumo',
    color='mes'
)

# Renderizando o gráfico com Streamlit
st.altair_chart(scatter_chart, use_container_width=True)

st.write(""" 
### Grafico de Barras
""")

# Criando o gráfico
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('ano:T', axis=alt.Axis(format='%Y')),
    y='consumo',
    color='mes'
)

# Mostrando o gráfico no Streamlit
st.altair_chart(chart, use_container_width=True)

st.write(""" 
### Grafico de Linha
Mostra o consumo por mes
""")

line_chart = alt.Chart(df).mark_line().encode(
    x='mes',
    y='consumo',
    tooltip=['mes', 'consumo']
).interactive()

# Renderizando o gráfico com Streamlit
st.altair_chart(line_chart, use_container_width=True)
