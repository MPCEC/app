import streamlit as st
import pickle
from datetime import date
import pandas as pd
import altair as alt
import plotly.express as px

st.title("MPCEC BR - Modelo Preditivo de Consumo Elétrico Coletivo Brasileiro")

st.write(""" 
O MPCEC BR - Modelo Preditivo de Consumo Elétrico Coletivo Brasileiro é um aplicativo que utiliza um modelo preditivo para estimar o consumo de energia elétrica coletivo no Brasil, considerando as informações fornecidas pelo usuário. O modelo utiliza um algoritmo de regressão linear para gerar uma previsão de consumo em Megawatts-hora (MWh) para um determinado mês e ano, levando em conta o estado do país e o tipo de consumo (residencial, industrial, comercial ou outros). Além disso, o usuário deve fornecer o número de consumidores na área de interesse.

Para utilizar o aplicativo, preencha o formulário com as informações solicitadas e aguarde a exibição do resultado. O consumo estimado de energia elétrica será calculado automaticamente após a inserção das informações pelo usuário. Lembre-se que o modelo é uma ferramenta para auxiliar na tomada de decisão e pode haver variações em relação ao consumo real.


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

ano_mes = st.date_input('Para começar selecione a data da previsão', min_value=date(2004, 1, 1), max_value=date(2050, 12, 31))
estado = st.selectbox('Agora o estado em que deseja tentar prever o consumo', list(mapeamento_estado.keys()))
st.write(""" 
### Qual o tipo de consumo que será previsto?

A seguir, apresentamos uma lista explicando os diferentes tipos de consumo de energia elétrica:

Total: Este é o consumo total de energia elétrica em um determinado período de tempo, que pode ser medido em megawatts-hora (MWh) ou quilowatts-hora (kWh). Ele representa a quantidade total de energia elétrica consumida por uma região, país ou até mesmo pelo mundo inteiro.

Cativo: O consumo cativo se refere ao consumo de energia elétrica por parte de consumidores que são obrigados a comprar eletricidade de uma concessionária específica em sua área geográfica, sem ter a opção de escolher o seu fornecedor de energia. Geralmente, ocorre em áreas em que há apenas uma concessionária fornecendo energia elétrica para a região, ou em situações em que as regulamentações impedem a entrada de novos fornecedores no mercado.

Residencial: O consumo residencial de energia elétrica ocorre em residências e lares, onde é utilizada para iluminação, aquecimento, refrigeração, cozimento de alimentos, entre outras atividades domésticas.

Industrial: O consumo industrial de energia elétrica ocorre em fábricas e indústrias, onde é utilizada para alimentar equipamentos, motores e outros processos de produção.

Comercial: O consumo comercial de energia elétrica ocorre em estabelecimentos comerciais, como lojas, escritórios, restaurantes e hotéis. É utilizada para iluminação, climatização, sistemas de segurança, entre outros.

Outros: O consumo de energia elétrica que não se enquadra nas categorias acima é classificado como "outros". Isso inclui o consumo de energia elétrica em instalações públicas, como iluminação de ruas e estradas, sistemas de transporte público e iluminação de monumentos, por exemplo.

""")

consumo_num = st.selectbox('E então, qual o tipo de consumo que será previsto?', list(mapeamento_consumo.keys()))
numero_consumidores = st.number_input('O número de consumidores é uma informação importante para o cálculo do consumo de energia elétrica estimado pelo MPCEC BR. Embora o número de consumidores não seja o fator mais influente na predição, ele ajuda a tornar a previsão mais precisa. Isso porque o modelo utiliza dados de consumo de energia elétrica coletivo, e não de indivíduos, e um número maior de consumidores pode proporcionar uma melhor estimativa do consumo total. No entanto, é importante ressaltar que a predição por número de consumidores pode variar dependendo das opções selecionadas acima no formulário, como o tipo de consumo, o estado e o mês/ano escolhidos. Por isso, é recomendado que o usuário insira o número mais próximo possível do total de consumidores na área de interesse para obter uma estimativa mais precisa do consumo de energia elétrica.  Lembre-se que o MPCEC BR é uma ferramenta de previsão e, portanto, as estimativas apresentadas podem variar em relação ao consumo real. O objetivo do aplicativo é fornecer informações úteis para a tomada de decisão e planejamento em relação ao consumo de energia elétrica coletivo no Brasil. Espero que ajude! ', value=1)

# Mapear valores selecionados para valores numéricos
sigla_uf = mapeamento_estado[estado]
tipo_consumo = mapeamento_consumo[consumo_num]

# Usar o modelo para fazer previsões
ano = ano_mes.year
mes = ano_mes.month
input_data = [[ano, mes, sigla_uf, tipo_consumo, numero_consumidores]]
prediction = model.predict(input_data)

# Exibir o resultado da previsão
st.write('### O consumo total de todo estado de ' + str(estado) + ' do ano ' + str(ano) + ' e mês ' + str(mes) + ' com número de consumidores de ' + str(numero_consumidores) + ' e o tipo de consumo ' + str(consumo_num) + ' em MWh é de:')
st.write(f"# {prediction[0]:,.0f} MWh")

st.write(""" 

# Histograma de consumo

Olá, bem-vindo ao nosso aplicativo de histogramas de consumo elétrico! Com essa ferramenta, você poderá visualizar o consumo de energia elétrica em um estado brasileiro em uma data específica.

Para utilizar o aplicativo, basta selecionar a data desejada no menu dropdown de seleção, que vai de janeiro de 2004 até dezembro de 2021, e o estado brasileiro em que você mora em outro menu dropdown.

Após selecionar essas informações, você poderá visualizar o histograma de consumo elétrico do estado selecionado na data escolhida. Isso pode ser útil para acompanhar o consumo de energia em sua região e identificar possíveis picos de consumo.

Aproveite essa ferramenta para se manter informado sobre o consumo de energia elétrica em sua região e contribuir para um uso mais consciente da energia elétrica!


""")

# Carrega o dataframe
df = pd.read_csv("novos_dados.csv")

# Carrega o dataframe
df = pd.read_csv("novos_dados.csv")

#GRAFICO DE AREA
data_inicial = date(2010, 1, 1)
mes_ano = st.date_input('Selecione a data do histograma', value=data_inicial, min_value=date(2004, 1, 1), max_value=date(2021, 12, 31))

ano = mes_ano.year
mes = mes_ano.month

estado_uf = st.selectbox('Selecione o estado:', list(mapeamento_estado.keys()))
sigla_uf = mapeamento_estado[estado_uf]

df_estado = df[df['sigla_uf'] == sigla_uf]
fig = px.area(df_estado, x="mes", y="consumo", title=f'Consumo de Energia em {estado_uf} por Mês Grafico de área')
st.plotly_chart(fig, use_container_width=True)

#GRAFICO DE BARRA
fig = px.bar(df[(df['ano'] == ano) & (df['mes'] == mes) & (df['sigla_uf'] == sigla_uf)], x="consumo", y="mes", title=f'Consumo de Energia em {estado_uf} por Mês Grafico de Barras')
st.plotly_chart(fig, use_container_width=True)
