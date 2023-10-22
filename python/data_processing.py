import pandas as pd
import requests
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_csv(symbol):
    logging.info(f'Iniciando leitura do CSV para {symbol}')
    url = f'https://www.cryptodatadownload.com/cdd/Binance_{symbol}BRL_d.csv'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        from io import StringIO
        data = StringIO(response.text)
        
        dataframe = pd.read_csv(data, skiprows=1)
        logging.info('CSV lido com sucesso.')

        # Se a coluna não for num faz substituição
        if not pd.api.types.is_numeric_dtype(dataframe[f'Volume {symbol}']):
            dataframe[f'Volume {symbol}'] = dataframe[f'Volume {symbol}'].str.replace('.', '').str.replace(',', '.').astype(float)
        if not pd.api.types.is_numeric_dtype(dataframe['Volume BRL']):
            dataframe['Volume BRL'] = dataframe['Volume BRL'].str.replace('.', '').str.replace(',', '.').astype(float) 

        logging.info('Dados processados com sucesso.')
        dataframe = dataframe.drop(['Date', 'Symbol', 'Unix'], axis=1)

        return dataframe

    except requests.HTTPError as http_err:
        logging.error(f'HTTP error: {http_err}')
    except requests.ConnectionError:
        logging.error('Falha ao estabelecer conexão.')
    except requests.Timeout:
        logging.error('Tempo atingido.')
    except requests.RequestException as err:
        logging.error(f'Ocorreu um erro: {err}')
    except Exception as e:
        logging.error(f'Ocorreu um erro durante a leitura do CSV: {e}')

def get_symbols():
    return ['ADA', 'AXS', 'BNB', 'BTC', 'BUSD', 'C98', 'CHZ', 'DOGE', 'DOT', 'ENJ', 'ETH', 'FIS', 'LINK', 'LTC', 'MATIC', 'SHIB', 'SOL', 'USDT', 'WIN', 'XRP']

def create_lagged_features(dataframe, lags=5):
    lagged_dataframes = [dataframe.shift(i) for i in range(lags + 1)]
    for i, lagged_dataframe in enumerate(lagged_dataframes):
        dataframe = pd.concat([dataframe, lagged_dataframe[['Open', 'High', 'Low', 'Close']].rename(columns=lambda x: f'{x}_lag_{i}')], axis=1)
    return dataframe.dropna()

def prepare_data(symbol):
    logging.info(f'Preparando dados para {symbol}')
    dataframe = read_csv(symbol)

    # Incluindo valores de OHLC dos últimos "n" dias
    dataframe = create_lagged_features(dataframe, 3)
    x = dataframe.drop('Close', axis=1)
    y = dataframe['Close']

    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.25)
    logging.info('Dados preparados com sucesso.')    
    return train_x, test_x, train_y, test_y
