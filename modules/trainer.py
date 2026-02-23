"""
Module 1: Model Trainer
Trains a RandomForest classifier on seizure dataset
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os


class SeizureModelTrainer:
    def __init__(self, dataset_path='datasets/seizure_dataset.csv'):
        self.dataset_path = dataset_path
        self.model = None
        self.scaler = None
        self.feature_columns = None
        
    def load_data(self):
        """Load and prepare the dataset"""
        print("Loading dataset...")
        df = pd.read_csv(self.dataset_path)
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        return df
    
    def prepare_features(self, df):
        """Prepare features and target variable"""
        # Assume last column is target, rest are features
        # Adjust based on your actual dataset structure
        if 'target' in df.columns:
            target_col = 'target'
        elif 'label' in df.columns:
            target_col = 'label'
        elif 'class' in df.columns:
            target_col = 'class'
        else:
            # Assume last column is target
            target_col = df.columns[-1]
        
        # Separate features and target
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        # Store feature columns for later use
        self.feature_columns = X.columns.tolist()
        
        print(f"\nFeatures: {len(X.columns)}")
        print(f"Target distribution:\n{y.value_counts()}")
        
        return X, y
    
    def train_model(self, X_train, y_train):
        """Train RandomForest classifier"""
        print("\nTraining RandomForest model...")
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train_scaled, y_train)
        print("Model training complete!")
        
        return X_train_scaled
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate model performance"""
        X_test_scaled = self.scaler.transform(X_test)
        y_pred = self.model.predict(X_test_scaled)
        
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\n{'='*50}")
        print(f"Model Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"{'='*50}")
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        return accuracy
    
    def save_model(self, model_dir='models'):
        """Save trained model and scaler"""
        os.makedirs(model_dir, exist_ok=True)
        
        model_path = os.path.join(model_dir, 'seizure_model.pkl')
        scaler_path = os.path.join(model_dir, 'scaler.pkl')
        features_path = os.path.join(model_dir, 'feature_columns.pkl')
        
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        joblib.dump(self.feature_columns, features_path)
        
        print(f"\nModel saved to: {model_path}")
        print(f"Scaler saved to: {scaler_path}")
        print(f"Features saved to: {features_path}")
    
    def run_training_pipeline(self):
        """Execute complete training pipeline"""
        try:
            # Load data
            df = self.load_data()
            
            # Prepare features
            X, y = self.prepare_features(df)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")
            
            # Train model
            self.train_model(X_train, y_train)
            
            # Evaluate model
            accuracy = self.evaluate_model(X_test, y_test)
            
            # Save model
            self.save_model()
            
            return accuracy
            
        except Exception as e:
            print(f"Error during training: {str(e)}")
            raise


if __name__ == "__main__":
    trainer = SeizureModelTrainer()
    trainer.run_training_pipeline()
