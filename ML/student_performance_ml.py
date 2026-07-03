import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

def main():
    # 1. Load Data
    print("Loading data...")
    df = pd.read_csv('dataset.txt')
    print(f"Data loaded. Shape: {df.shape}")

    # 2. Basic Cleaning
    print("Cleaning data...")
    # Drop rows without the target variable
    df = df.dropna(subset=['passed'])

    # Fill missing scores with 0 (assuming absent/excused implies no score collected yet or 0 for the model)
    score_cols = ['quiz1_score', 'quiz2_score', 'midterm_score', 'final_exam_score', 'total_score']
    for col in score_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    # 3. EDA
    print("Performing EDA...")
    os.makedirs('plots', exist_ok=True)
    
    # Plot target distribution
    plt.figure(figsize=(6, 4))
    sns.countplot(x='passed', data=df)
    plt.title('Distribution of Passed (1) vs Failed (0)')
    plt.savefig('plots/target_distribution.png')
    plt.close()

    # Plot passing rate by academic year
    if 'academic_year' in df.columns:
        plt.figure(figsize=(8, 5))
        sns.barplot(x='academic_year', y='passed', data=df, errorbar=None)
        plt.title('Passing Rate by Academic Year')
        plt.savefig('plots/passing_rate_by_year.png')
        plt.close()

    # Correlation heatmap of numeric features
    numeric_df = df.select_dtypes(include=[np.number])
    plt.figure(figsize=(12, 10))
    sns.heatmap(numeric_df.corr(), annot=False, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.savefig('plots/correlation_matrix.png')
    plt.close()

    # 4. Feature Selection & Preprocessing
    print("Preparing features...")
    # Drop trivial columns (e.g., total_score and final_exam_score make the prediction too easy)
    # Also drop IDs
    drop_cols = ['passed', 'total_score', 'final_exam_score', 'professor_id', 'course_code', 'course_name', 'semester_name']
    
    # Check if we should drop quiz/midterm statuses since they might just mirror the score being 0
    # Let's keep them, as they are categorical
    
    X = df.drop(columns=[c for c in drop_cols if c in df.columns])
    y = df['passed']

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
    # We use a random split here. If chronological is preferred, we could sort by enroll_year/semester.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")

    # 6. Model Training
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1),
        'HistGradientBoosting': HistGradientBoostingClassifier(random_state=42)
    }

    best_model = None
    best_acc = 0
    best_name = ""

    print("Training models...")
    for name, model in models.items():
        clf = Pipeline(steps=[('preprocessor', preprocessor),
                              ('classifier', model)])
        
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        print(f"\n--- {name} ---")
        print(f"Accuracy: {acc:.4f}")
        print(classification_report(y_test, y_pred))
        
        # Save confusion matrix plot
        cm = confusion_matrix(y_test, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Failed', 'Passed'])
        disp.plot(cmap='Blues')
        plt.title(f'{name} Confusion Matrix')
        plt.savefig(f'plots/{name.replace(" ", "_")}_cm.png')
        plt.close()

        if acc > best_acc:
            best_acc = acc
            best_model = clf
            best_name = name

    print(f"\nBest Model: {best_name} with Accuracy: {best_acc:.4f}")
    
    # 7. Save the best model
    model_path = 'best_student_model.pkl'
    joblib.dump(best_model, model_path)
    print(f"Best model saved to {model_path}")

if __name__ == '__main__':
    main()
