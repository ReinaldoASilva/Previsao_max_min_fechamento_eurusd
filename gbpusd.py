import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
from tvDatafeed import TvDatafeed, Interval
import numpy as numpy

def prever_proximo_dia(gbpusd):
    # Transformar os dados em um DataFrame
    gbpusd = pd.DataFrame(gbpusd)
    
    # Calcular o preço de fechamento médio
    gbpusd['Preco Medio'] = (gbpusd['high'] + gbpusd['low']) / 2

    # Criar colunas com os preços do dia seguinte (shift(-1))
    gbpusd['Proximo dia max'] = gbpusd['high'].shift(-1)
    gbpusd['Proximo dia min'] = gbpusd['low'].shift(-1)
    gbpusd['Proximo dia close'] = gbpusd['close'].shift(-1)
    gbpusd['Proximo dia Preco Medio'] = gbpusd['Preco Medio'].shift(-1)

    gbpusd = gbpusd.dropna()

    # Substituir NaN por 0
    gbpusd.fillna(0, inplace=True)

    # Dividir os dados em variáveis de entrada (X) e saída (y) para max, min, close e preco medio
    X = gbpusd[['Preco Medio']]
    y_max = gbpusd[['Proximo dia max']]
    y_min = gbpusd[['Proximo dia min']]
    y_close = gbpusd[['Proximo dia close']]
    y_preco_medio = gbpusd[['Proximo dia Preco Medio']]

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
    previsao_max = modelo_max.predict([[gbpusd['close'].iloc[-1]]])[0][0]
    previsao_min = modelo_min.predict([[gbpusd['close'].iloc[-1]]])[0][0]
    previsao_close = modelo_close.predict([[gbpusd['close'].iloc[-1]]])[0][0]
    previsao_preco_medio = modelo_preco_medio.predict([[gbpusd['close'].iloc[-1]]])[0][0]

    return previsao_max, previsao_min, previsao_close, previsao_preco_medio

# Exemplo de uso da função
tv = TvDatafeed()
# Baixar dados históricos
gbpusd = tv.get_hist(symbol='gbpusd', exchange='activtrades', interval=Interval.in_daily, n_bars=10000)

# Chamar a função para fazer a previsão
previsao_max, previsao_min, previsao_close, previsao_preco_medio = prever_proximo_dia(gbpusd)

# Imprimir os resultados das previsões
print(f"Previsão da máxima do próximo dia: {previsao_max:.2f}")
print(f"Previsão da mínima do próximo dia: {previsao_min:.2f}")
print(f"Previsão do fechamento do próximo dia: {previsao_close:.2f}")
print(f"Previsão do preço médio do próximo dia: {previsao_preco_medio:.2f}")

