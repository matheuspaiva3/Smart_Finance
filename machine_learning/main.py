import logging
from prediction import predict_for_all_symbols

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    try:
        logging.info('Iniciando predição para todos os símbolos.')
        predict_for_all_symbols()
    except Exception as err:
        logging.error(f'Ocorreu um erro inesperado: {err}')
