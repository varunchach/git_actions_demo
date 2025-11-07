import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
import joblib
import json
import pytest

def test_model_predictions():
    # Load the test data
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name='target')
    
    # Load the model
    model = joblib.load('model.joblib')
    
    # Make predictions
    predictions = model.predict(X)
    
    # Basic validation
    assert len(predictions) == len(y), "Prediction length doesn't match target length"

def test_model_accuracy():
    # Load the test data
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name='target')
    
    # Load the model
    model = joblib.load('model.joblib')
    
    # Check accuracy
    accuracy = model.score(X, y)
    assert accuracy > 0.8, f"Model accuracy {accuracy} is below threshold of 0.8"