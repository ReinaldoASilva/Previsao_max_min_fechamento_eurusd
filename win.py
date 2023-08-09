import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
from tvDatafeed import TvDatafeed, Interval
import numpy as numpy

def prever_proximo_dia(win):
    # Transformar os dados em um DataFrame
    win = pd.DataFrame(win)
    
    # Calcular o preço de fechamento médio
    win['Preco Medio'] = (win['high'] + win['low']) / 2

    # Criar colunas com os preços do dia seguinte (shift(-1))
    win['Proximo dia max'] = win['high'].shift(-1)
    win['Proximo dia min'] = win['low'].shift(-1)
    win['Proximo dia close'] = win['close'].shift(-1)
    win['Proximo dia Preco Medio'] = win['Preco Medio'].shift(-1)

    win = win.dropna()

    # Substituir NaN por 0
    win.fillna(0, inplace=True)

    # Dividir os dados em variáveis de entrada (X) e saída (y) para max, min, close e preco medio
    X = win[['Preco Medio']]
    y_max = win[['Proximo dia max']]
    y_min = win[['Proximo dia min']]
    y_close = win[['Proximo dia close']]
    y_preco_medio = win[['Proximo dia Preco Medio']]

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
    previsao_max = modelo_max.predict([[win['close'].iloc[-1]]])[0][0]
    previsao_min = modelo_min.predict([[win['close'].iloc[-1]]])[0][0]
    previsao_close = modelo_close.predict([[win['close'].iloc[-1]]])[0][0]
    previsao_preco_medio = modelo_preco_medio.predict([[win['close'].iloc[-1]]])[0][0]

    return previsao_max, previsao_min, previsao_close, previsao_preco_medio

# Exemplo de uso da função
tv = TvDatafeed()
# Baixar dados históricos
win = tv.get_hist(symbol='win1!', exchange='bmfbovespa', interval=Interval.in_daily, n_bars=10000)

# Chamar a função para fazer a previsão
previsao_max, previsao_min, previsao_close, previsao_preco_medio = prever_proximo_dia(win)

# Imprimir os resultados das previsões
print(f"Previsão da máxima do próximo dia: {previsao_max:.2f}")
print(f"Previsão da mínima do próximo dia: {previsao_min:.2f}")
print(f"Previsão do fechamento do próximo dia: {previsao_close:.2f}")
print(f"Previsão do preço médio do próximo dia: {previsao_preco_medio:.2f}")

