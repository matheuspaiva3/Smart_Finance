import os
import pickle
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_directory(dir_name):
    logging.info(f'Criando diretório {dir_name}')    
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def save_model(model, filename):
    logging.info(f'Salvando modelo {model} no arquivo {filename}')    
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
