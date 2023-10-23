from sklearn.metrics import r2_score
from models_tuning import tune_linear_regression
from models_tuning import tune_random_forest
from models_tuning import tune_svr
from models_tuning import tune_gradient_boost
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def tuned_linear_regression_test(train_x, test_x, train_y, test_y):
    tuned_model = tune_linear_regression(train_x, train_y)
    tuned_prediction = tuned_model.predict(test_x)

    print(f'Tuned Linear Regression score: {r2_score(test_y, tuned_prediction):.6%}')
    return tuned_prediction

def tuned_random_forest_test(train_x, test_x, train_y, test_y):
    tuned_model = tune_random_forest(train_x, train_y)
    tuned_prediction = tuned_model.predict(test_x)

    print(f'Tuned Random Forest score: {r2_score(test_y, tuned_prediction):.6%}')
    return tuned_prediction

def tuned_support_vector_test(train_x, test_x, train_y, test_y):
    tuned_model = tune_svr(train_x, train_y)
    tuned_prediction = tuned_model.predict(test_x)

    print(f'Tuned SVR score: {r2_score(test_y, tuned_prediction):.6%}')
    return tuned_prediction

def tuned_gradient_boost_test(train_x, test_x, train_y, test_y):
    tuned_model = tune_gradient_boost(train_x, train_y)
    tuned_prediction = tuned_model.predict(test_x)

    print(f'Tuned Gradient Boost score: {r2_score(test_y, tuned_prediction):.6%}')
    return tuned_prediction
