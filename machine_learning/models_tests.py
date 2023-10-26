import logging
from sklearn.metrics import r2_score, mean_absolute_error

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def evaluate_model(model, train_x, test_x, train_y, test_y):
    logging.info(f'Avaliando modelo: {model}')

    model.fit(train_x, train_y)
    prediction = model.predict(test_x)

    score = r2_score(test_y, prediction)
    mae = mean_absolute_error(test_y, prediction)

    return prediction, score, mae

def evaluate_tuned_models(tuned_models, train_x, test_x, train_y, test_y):
    predictions = {}
    scores = {}
    maes = {}

    for model_name, model in tuned_models.items():
        pred, score, mae = evaluate_model(model, train_x, test_x, train_y, test_y)
        print(f"{model_name} - R2 Score: {score:.6%}, MAE: {mae}")

        predictions[model_name] = pred
        scores[model_name] = score
        maes[model_name] = mae

    return predictions, scores, maes
