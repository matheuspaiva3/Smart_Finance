from prediction import predict_for_all_symbols
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    try:
        logging.info('Iniciando predição para todos os símbolos.')    
        predict_for_all_symbols()
    except Exception as e:
        logging.error(f'Ocorreu um erro inesperado: {e}')
