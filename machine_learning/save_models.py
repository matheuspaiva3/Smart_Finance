import os
import pickle

def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def save_model(model, filename):
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
