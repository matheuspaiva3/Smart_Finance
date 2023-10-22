# app.py
from flask import Flask, jsonify
from prediction import predict_for_all_symbols

app = Flask(__name__)

@app.route('/predictions', methods=['GET'])
def get_predictions():
    predictions = predict_for_all_symbols()
    return jsonify(predictions)
