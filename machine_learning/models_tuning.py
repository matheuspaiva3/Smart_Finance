import logging
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def tune_model(model, train_x, train_y, parameters, n_iter, needs_scaling=False):
    logging.info(f'Iniciando ajuste para o modelo: {model}...')

    if needs_scaling:
        scaler = StandardScaler()
        train_x = scaler.fit_transform(train_x)

    random_search = RandomizedSearchCV(model, parameters, n_iter=n_iter, cv=5, scoring='r2', random_state=42, n_jobs=-1)
    random_search.fit(train_x, train_y)

    logging.info('Modelo ajustado com sucesso. Retornando o melhor estimador.')

    return random_search.best_estimator_

def tune_all_models(train_x, train_y):
    tuned_models = {}

    tuned_models["Linear Regression"] = tune_model(LinearRegression(), train_x, train_y, {'fit_intercept': [True, False]}, 2)

    tuned_models["Random Forest"] = tune_model(RandomForestRegressor(), train_x, train_y, {'max_depth': [None, 10, 20], 'n_estimators': [50, 100, 150]}, 2)

    tuned_models["Gradient Boost"] = tune_model(GradientBoostingRegressor(), train_x, train_y, {'max_depth': [3, 4, 5], 'n_estimators': [50, 100, 150]}, 1)

    return tuned_models
