import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

def generate_synthetic_data(num_samples=1000):
    np.random.seed(42)
    
    # Generate random features
    study_hours = np.random.uniform(0, 8, num_samples)
    work_hours = np.random.uniform(0, 10, num_samples)
    screen_time = np.random.uniform(1, 14, num_samples)
    distraction_time = np.random.uniform(0, 5, num_samples)
    sleep_hours = np.random.normal(7, 1.5, num_samples)
    sleep_hours = np.clip(sleep_hours, 2, 12) # Clamp between 2 and 12
    
    # Feature engineering (prevent division by zero)
    productivity_ratio = (study_hours + work_hours) / (screen_time + 0.1)
    distraction_ratio = distraction_time / (study_hours + work_hours + 0.1)
    consistency_score = sleep_hours / 8.0
    
    # Calculate target variable (productivity_score 0-100)
    # A simple formula combining the features with some noise
    base_score = (
        (study_hours * 5) + 
        (work_hours * 5) - 
        (distraction_time * 8) - 
        (screen_time * 2) + 
        (sleep_hours * 4)
    )
    
    # Normalize base score to be roughly 0-100
    # Min possible roughly around -50, Max around 100+
    # We'll just rescale it and add noise
    min_val = np.min(base_score)
    max_val = np.max(base_score)
    
    normalized_score = 100 * (base_score - min_val) / (max_val - min_val)
    productivity_score = normalized_score + np.random.normal(0, 5, num_samples)
    productivity_score = np.clip(productivity_score, 0, 100)
    
    data = pd.DataFrame({
        'study_hours': study_hours,
        'work_hours': work_hours,
        'screen_time': screen_time,
        'distraction_time': distraction_time,
        'sleep_hours': sleep_hours,
        'productivity_ratio': productivity_ratio,
        'distraction_ratio': distraction_ratio,
        'consistency_score': consistency_score,
        'productivity_score': productivity_score
    })
    
    return data

def train_and_save_model():
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/synthetic_data.csv', index=False)
    print("Data saved to data/synthetic_data.csv")
    
    features = [
        'study_hours', 'work_hours', 'screen_time', 
        'distraction_time', 'sleep_hours', 
        'productivity_ratio', 'distraction_ratio', 'consistency_score'
    ]
    
    X = df[features]
    y = df['productivity_score']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    score = model.score(X_test, y_test)
    print(f"Model trained with R^2 score: {score:.4f}")
    
    # Ensure model directory exists
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/rf_model.joblib')
    print("Model saved to model/rf_model.joblib")

if __name__ == '__main__':
    train_and_save_model()
