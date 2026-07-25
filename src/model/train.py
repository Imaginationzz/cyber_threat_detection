import pandas as pd
import xgboost as xgb
import mlflow
import mlflow.xgboost
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import os

# Set MLflow tracking URI (Local folder for now)
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("Cyber_Threat_Classification")

def train_model():
    print("Loading synthetic data...")
    # Navigate up from src/model to the data folder
    data_path = os.path.join(os.path.dirname(__file__), '../../data/synthetic_network_traffic.csv')
    df = pd.read_csv(data_path)

    # 1. Data Preprocessing
    # We drop 'timestamp' and 'source_ip' for this baseline model as they require advanced feature engineering
    X = df[['dest_port', 'packet_size', 'failed_logins', 'status_code']]
    y = df['label']

    # Encode our text labels (Safe, DDoS, etc.) into numbers (0, 1, 2...)
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    # Split into training (80%) and testing (20%) datasets
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # 2. Start MLflow Run
    with mlflow.start_run():
        print("Training XGBoost model...")
        
        # Define model parameters
        params = {
            "objective": "multi:softmax",
            "num_class": len(encoder.classes_),
            "max_depth": 5,
            "learning_rate": 0.1,
            "n_estimators": 100
        }
        
        # Log parameters to MLflow
        mlflow.log_params(params)

        # Train the model
        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train)

        # 3. Evaluate the Model
        predictions = model.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        
        print(f"Model Accuracy: {acc:.4f}")
        
        # Log metrics to MLflow
        mlflow.log_metric("accuracy", acc)
        
        # 4. Save (Log) the Model to MLflow
        mlflow.xgboost.log_model(model, "xgboost_threat_model")
        
        print("\nClassification Report:")
        print(classification_report(y_test, predictions, target_names=encoder.classes_))
        print("\nModel training complete and logged to MLflow!")

if __name__ == "__main__":
    train_model()