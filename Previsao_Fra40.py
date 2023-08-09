import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
from tvDatafeed import TvDatafeed, Interval
import numpy as numpy

def prever_proximo_dia(fra40):
    # Transformar os dados em um DataFrame
    fra40 = pd.DataFrame(fra40)
    
    # Calcular o preço de fechamento médio
    fra40['Preco Medio'] = (fra40['high'] + fra40['low']) / 2

    # Criar colunas com os preços do dia seguinte (shift(-1))
    fra40['Proximo dia max'] = fra40['high'].shift(-1)
    fra40['Proximo dia min'] = fra40['low'].shift(-1)
    fra40['Proximo dia close'] = fra40['close'].shift(-1)
    fra40['Proximo dia Preco Medio'] = fra40['Preco Medio'].shift(-1)

    fra40 = fra40.dropna()

    # Substituir NaN por 0
    fra40.fillna(0, inplace=True)

    # Dividir os dados em variáveis de entrada (X) e saída (y) para max, min, close e preco medio
    X = fra40[['Preco Medio']]
    y_max = fra40[['Proximo dia max']]
    y_min = fra40[['Proximo dia min']]
    y_close = fra40[['Proximo dia close']]
    y_preco_medio = fra40[['Proximo dia Preco Medio']]

    # Criar modelos de regressão linear para max, min, close e preco medio
    modelo_max = LinearRegression()
    modelo_min = LinearRegression()
    modelo_close = LinearRegression()
    modelo_preco_medio = LinearRegression()

    # Treinar os modelos
    modelo_max.fit(X, y_max)
    modelo_min.fit(X, y_min)
    modelo_close.fit(X, y_close)
    modelo_preco_medio.fit(X, y_preco_medio)

    # Fazer as previsões para max, min, close e preco medio do próximo dia
    previsao_max = modelo_max.predict([[fra40['close'].iloc[-1]]])[0][0]
    previsao_min = modelo_min.predict([[fra40['close'].iloc[-1]]])[0][0]
    previsao_close = modelo_close.predict([[fra40['close'].iloc[-1]]])[0][0]
    previsao_preco_medio = modelo_preco_medio.predict([[fra40['close'].iloc[-1]]])[0][0]

    return previsao_max, previsao_min, previsao_close, previsao_preco_medio

# Exemplo de uso da função
tv = TvDatafeed()
# Baixar dados históricos
fra40 = tv.get_hist(symbol='fra40', exchange='pepperstone', interval=Interval.in_daily, n_bars=10000)

# Chamar a função para fazer a previsão
previsao_max, previsao_min, previsao_close, previsao_preco_medio = prever_proximo_dia(fra40)

# Imprimir os resultados das previsões
print(f"Previsão da máxima do próximo dia: {previsao_max:.2f}")
print(f"Previsão da mínima do próximo dia: {previsao_min:.2f}")
print(f"Previsão do fechamento do próximo dia: {previsao_close:.2f}")
print(f"Previsão do preço médio do próximo dia: {previsao_preco_medio:.2f}")

