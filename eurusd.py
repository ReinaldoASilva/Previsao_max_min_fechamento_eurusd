import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
import numpy as numpy
import pandas_datareader.data as pdr
import yfinance as yf


def prever_proximo_dia(eurusd):
    # Transformar os dados em um DataFrame
    eurusd = pd.DataFrame(eurusd)
    
    # Calcular o preço de fechamento médio
    eurusd['Adj Close'] = (eurusd['High'] + eurusd['Low']) / 2

    # Criar colunas com os preços do dia seguinte (shift(-1))
    eurusd['Proximo dia max'] = eurusd['High'].shift(-1)
    eurusd['Proximo dia min'] = eurusd['Low'].shift(-1)
    eurusd['Proximo dia Close'] = eurusd['Close'].shift(-1)
    eurusd['Proximo dia Preco Medio'] = eurusd['Adj Close'].shift(-1)

    eurusd = eurusd.dropna()

    # Substituir NaN por 0
    eurusd.fillna(0, inplace=True)

    # Dividir os dados em variáveis de entrada (X) e saída (y) para max, min, Close e preco medio
    X = eurusd[['Adj Close']]
    y_max = eurusd[['Proximo dia max']]
    y_min = eurusd[['Proximo dia min']]
    y_Close = eurusd[['Proximo dia Close']]
    y_preco_medio = eurusd[['Proximo dia Preco Medio']]

    # Criar modelos de regressão linear para max, min, Close e preco medio
    modelo_max = LinearRegression()
    modelo_min = LinearRegression()
    modelo_Close = LinearRegression()
    modelo_preco_medio = LinearRegression()

    # Treinar os modelos
    modelo_max.fit(X, y_max)
    modelo_min.fit(X, y_min)
    modelo_Close.fit(X, y_Close)
    modelo_preco_medio.fit(X, y_preco_medio)

    # Fazer as previsões para max, min, Close e preco medio do próximo dia
    previsao_max = modelo_max.predict([[eurusd['Close'].iloc[-1]]])[0][0]
    previsao_min = modelo_min.predict([[eurusd['Close'].iloc[-1]]])[0][0]
    previsao_Close = modelo_Close.predict([[eurusd['Close'].iloc[-1]]])[0][0]
    previsao_preco_medio = modelo_preco_medio.predict([[eurusd['Close'].iloc[-1]]])[0][0]

    return previsao_max, previsao_min, previsao_Close, previsao_preco_medio



# Defina o ticker do ativo que você deseja importar
ticker = "EURUSD=X"  # Exemplo: Apple Inc.

# Obtenha a data atual
data_atual = datetime.today().strftime('%Y-%m-%d')

# Use a função download() para importar os dados
eurusd = yf.download(ticker, start="2021-01-01", end=data_atual)


# Chamar a função para fazer a previsão
previsao_max, previsao_min, previsao_Close, previsao_preco_medio = prever_proximo_dia(eurusd)

# Imprimir os resultados das previsões
print(f"Previsão da máxima do próximo dia: {previsao_max:.2f}")
print(f"Previsão da mínima do próximo dia: {previsao_min:.2f}")
print(f"Previsão do fechamento do próximo dia: {previsao_Close:.2f}")
print(f"Previsão do preço médio do próximo dia: {previsao_preco_medio:.2f}")

