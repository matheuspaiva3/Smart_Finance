import logging
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from scipy.stats import norm
from data_processing import prepare_data, get_symbols
from models_tuning import tune_all_models
from models_tests import evaluate_tuned_models
from models_tests import evaluate_model

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_confidence_interval(predictions, actuals, alpha=0.05):
    residuals = actuals - predictions
    residual_std = np.std(residuals)

    return predictions - norm.ppf(1 - alpha/2) * residual_std, predictions + norm.ppf(1 - alpha/2) * residual_std

def ensemble_decision(predictions, scores, test_y):
    buy_votes = 0
    valid_models = 0

    for model_name, pred in predictions.items():
        # Ignora modelos com R2 Score negativo
        if scores[model_name] < 0:
            continue

        accuracy = np.mean((pred > test_y.iloc[-1]) == (test_y.values > test_y.iloc[-1]))

        if accuracy >= 0.6:
            valid_models += 1

            if pred[-1] > test_y.iloc[-1]:
                buy_votes += 1

    if valid_models == 0:
        return "Sem recomendação para o ativo."

    return 'COMPRA' if buy_votes > valid_models / 2 else 'VENDA'

def predict_probability(predictions, test_y):
    above_last_close = sum(1 for pred in predictions if pred[-1] > test_y.iloc[-1])
    total_models = len(predictions)

    return above_last_close / total_models

def test_all_models(train_x, test_x, train_y, test_y):
    models = [
        LinearRegression(),
        RandomForestRegressor(),
        GradientBoostingRegressor(),
    ]

    trained_models = []
    model_names = ["linear_regression", "random_forest", "gradient_boost"]
    predictions = []

    for symbol in crypto_symbols:
        train_x, test_x, train_y, test_y = prepare_data(symbol)
        print(f'Testando para: {symbol}BRL...')

        trained_models = test_all_models(train_x, test_x, train_y, test_y)

    for model, name in zip(models, model_names):
        pred, score, mae = evaluate_model(model, train_x, test_x, train_y, test_y)

        logging.info(f'{name} score: {score:.6%}')
        logging.info(f'MAE: {mae}')

        predictions.append(pred)
        trained_models.append(model)

    for model in tuned_models:
        pred = model.predict(test_x)
        predictions.append(pred)
        trained_models.append(model)

    tuned_models = tune_all_models(train_x, train_y)
    tuned_predictions = evaluate_tuned_models(tuned_models, train_x, test_x, train_y, test_y)

    all_predictions = list(predictions.values()) + list(tuned_predictions.values())
    decision_ensemble = ensemble_decision(all_predictions, test_y)
    print(f'Ensemble Decision: {decision_ensemble}')

    buy_probability = predict_probability(all_predictions, test_y)
    print(f"Probability of an uptrend based on all models: {buy_probability:.2%}")

    return trained_models

crypto_symbols = [
    'ADA', 'AXS', 'BNB', 'BTC',
    'BUSD', 'C98', 'CHZ', 'DOGE',
    'DOT', 'ENJ', 'ETH', 'FIS',
    'LINK', 'LTC', 'MATIC', 'SHIB',
    'SOL', 'USDT', 'WIN', 'XRP',
]

def predict_for_all_symbols():
    symbols = get_symbols()
    recommendations = {}

    for symbol in symbols:
        print(f'\nAtivo: {symbol}...')

        train_x, test_x, train_y, test_y = prepare_data(symbol)
        tuned_models = tune_all_models(train_x, train_y)

        predictions, scores, maes = evaluate_tuned_models(tuned_models, train_x, test_x, train_y, test_y)
        valid_models = [model for model, score in scores.items() if score > 0 and maes[model] < 10]

        valid_predictions = {model: predictions[model] for model in valid_models}
        decision_ensemble = ensemble_decision(valid_predictions, scores, test_y)

        print(f'Recomendação da Smart Finance para {symbol}BRL: {decision_ensemble}\n')
        recommendations[symbol] = decision_ensemble

    return recommendations

if __name__ == "__main__":
    predict_for_all_symbols()
