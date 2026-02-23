"""
Module 2: Predictor
Loads trained model and makes predictions
"""
import joblib
import numpy as np
import pandas as pd
import os


class SeizurePredictor:
    def __init__(self, model_dir='models'):
        self.model_dir = model_dir
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.class_mapping = {
            0: 'NORMAL',
            1: 'PREICTAL',
            2: 'SEIZURE'
        }
        self.load_model()
    
    def load_model(self):
        """Load trained model, scaler, and feature columns"""
        try:
            model_path = os.path.join(self.model_dir, 'seizure_model.pkl')
            scaler_path = os.path.join(self.model_dir, 'scaler.pkl')
            features_path = os.path.join(self.model_dir, 'feature_columns.pkl')
            
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.feature_columns = joblib.load(features_path)
            
            print("Model loaded successfully!")
            
        except FileNotFoundError as e:
            print(f"Error: Model files not found. Please train the model first.")
            raise
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
    
    def prepare_input(self, features):
        """Prepare input features for prediction"""
        if isinstance(features, dict):
            # Convert dict to DataFrame
            df = pd.DataFrame([features])
        elif isinstance(features, pd.DataFrame):
            df = features
        elif isinstance(features, np.ndarray):
            df = pd.DataFrame(features, columns=self.feature_columns)
        else:
            raise ValueError("Features must be dict, DataFrame, or numpy array")
        
        # Ensure all required features are present
        missing_features = set(self.feature_columns) - set(df.columns)
        if missing_features:
            for feat in missing_features:
                df[feat] = 0  # Fill missing features with 0
        
        # Select only required features in correct order
        df = df[self.feature_columns]
        
        return df
    
    def predict(self, features):
        """Make prediction on input features"""
        try:
            # Prepare input
            df = self.prepare_input(features)
            
            # Scale features
            features_scaled = self.scaler.transform(df)
            
            # Get prediction
            prediction = self.model.predict(features_scaled)[0]
            probabilities = self.model.predict_proba(features_scaled)[0]
            
            # Get class name
            prediction_class = self.class_mapping.get(prediction, f"CLASS_{prediction}")
            
            # Get confidence score
            confidence = float(probabilities[prediction]) * 100
            
            # Determine risk level
            risk_level = self.get_risk_level(prediction_class, confidence)
            
            # Create result dictionary
            result = {
                'prediction': prediction_class,
                'confidence': confidence,
                'risk_level': risk_level,
                'probabilities': {
                    self.class_mapping.get(i, f"CLASS_{i}"): float(prob * 100)
                    for i, prob in enumerate(probabilities)
                },
                'explanation': self.get_explanation(prediction_class, confidence)
            }
            
            return result
            
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            raise
    
    def get_risk_level(self, prediction_class, confidence):
        """Determine risk level based on prediction and confidence"""
        if prediction_class == 'SEIZURE':
            if confidence >= 80:
                return 'HIGH'
            elif confidence >= 60:
                return 'MEDIUM'
            else:
                return 'MEDIUM'
        elif prediction_class == 'PREICTAL':
            if confidence >= 70:
                return 'MEDIUM'
            else:
                return 'LOW'
        else:  # NORMAL
            return 'LOW'
    
    def get_explanation(self, prediction_class, confidence):
        """Generate explanation for the prediction"""
        explanations = {
            'NORMAL': f"The EEG pattern appears normal with {confidence:.1f}% confidence. No seizure activity detected.",
            'PREICTAL': f"Pre-seizure state detected with {confidence:.1f}% confidence. This indicates potential seizure risk. Monitor closely and consult a neurologist.",
            'SEIZURE': f"Seizure activity detected with {confidence:.1f}% confidence. Immediate medical attention recommended. Contact emergency services if experiencing symptoms."
        }
        return explanations.get(prediction_class, "Unable to generate explanation.")
    
    def predict_batch(self, features_list):
        """Make predictions on multiple samples"""
        results = []
        for features in features_list:
            result = self.predict(features)
            results.append(result)
        return results


if __name__ == "__main__":
    # Test predictor
    predictor = SeizurePredictor()
    
    # Create dummy features for testing
    dummy_features = {col: np.random.randn() for col in predictor.feature_columns}
    
    result = predictor.predict(dummy_features)
    print("\nPrediction Result:")
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.2f}%")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Explanation: {result['explanation']}")
