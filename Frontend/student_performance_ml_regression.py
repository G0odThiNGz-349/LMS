import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def main():
    # 1. Load Data
    print("Loading data...")
    df = pd.read_csv('dataset.txt')
    print(f"Data loaded. Shape: {df.shape}")

    # 2. Basic Cleaning
    print("Cleaning data...")
    # Drop rows without the target variable (total_score)
    df = df.dropna(subset=['total_score'])

    # Fill missing scores with 0
    score_cols = ['quiz1_score', 'quiz2_score', 'midterm_score']
    for col in score_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    # 3. EDA specific to Regression
    print("Performing EDA for Regression...")
    os.makedirs('plots_regression', exist_ok=True)
    
    # Plot target distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df['total_score'], bins=30, kde=True)
    plt.title('Distribution of Total Scores')
    plt.xlabel('Total Score')
    plt.ylabel('Frequency')
    plt.savefig('plots_regression/total_score_distribution.png')
    plt.close()

    # 4. Feature Selection & Preprocessing
    print("Preparing features...")
    # We drop 'passed' and 'final_exam_score' so the model predicts total_score before the final exam happens
    drop_cols = ['total_score', 'passed', 'final_exam_score', 'professor_id', 'course_code', 'course_name', 'semester_name']
    
    X = df.drop(columns=[c for c in drop_cols if c in df.columns])
    y = df['total_score']

    # Identify column types
    numeric_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=[np.number]).columns.tolist()

    print(f"Numeric features: {len(numeric_features)}")
    print(f"Categorical features: {len(categorical_features)}")

    # Define preprocessing steps
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # 5. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")

    # 6. Model Training
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest Regressor': RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1),
        'HistGradientBoosting Regressor': HistGradientBoostingRegressor(random_state=42)
    }

    best_model = None
    best_r2 = -float('inf')
    best_name = ""

    print("Training models...")
    for name, model in models.items():
        clf = Pipeline(steps=[('preprocessor', preprocessor),
                              ('regressor', model)])
        
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"\n--- {name} ---")
        print(f"RMSE: {rmse:.4f}")
        print(f"MAE: {mae:.4f}")
        print(f"R2 Score: {r2:.4f}")
        
        # Save actual vs predicted plot
        plt.figure(figsize=(6, 6))
        plt.scatter(y_test, y_pred, alpha=0.1)
        plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
        plt.xlabel('Actual Total Score')
        plt.ylabel('Predicted Total Score')
        plt.title(f'{name}\nActual vs Predicted')
        plt.savefig(f'plots_regression/{name.replace(" ", "_")}_actual_vs_pred.png')
        plt.close()

        if r2 > best_r2:
            best_r2 = r2
            best_model = clf
            best_name = name

    print(f"\nBest Model: {best_name} with R2 Score: {best_r2:.4f}")
    
    # 7. Save the best model
    model_path = 'best_student_model_regression.pkl'
    joblib.dump(best_model, model_path)
    print(f"Best model saved to {model_path}")

if __name__ == '__main__':
    main()
