"""
Advanced CNN + LSTM Model for Seizure Detection
Deep learning model for improved accuracy (optional upgrade from RandomForest)
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Note: TensorFlow/Keras are optional dependencies
# Install with: pip install tensorflow
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("TensorFlow not available. Install with: pip install tensorflow")


class CNNLSTMSeizureModel:
    """
    CNN + LSTM hybrid model for seizure detection
    CNN extracts spatial features, LSTM captures temporal patterns
    """
    
    def __init__(self, input_shape=(100, 1), num_classes=3):
        """
        Initialize CNN-LSTM model
        
        Args:
            input_shape: Shape of input data (timesteps, features)
            num_classes: Number of output classes (3: Normal, Preictal, Seizure)
        """
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is required for CNN-LSTM model")
        
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = None
        self.scaler = StandardScaler()
        self.history = None
    
    def build_model(self):
        """Build CNN + LSTM architecture"""
        model = models.Sequential([
            # CNN layers for feature extraction
            layers.Conv1D(64, kernel_size=3, activation='relu', input_shape=self.input_shape),
            layers.BatchNormalization(),
            layers.MaxPooling1D(pool_size=2),
            layers.Dropout(0.3),
            
            layers.Conv1D(128, kernel_size=3, activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(pool_size=2),
            layers.Dropout(0.3),
            
            layers.Conv1D(256, kernel_size=3, activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(pool_size=2),
            layers.Dropout(0.3),
            
            # LSTM layers for temporal patterns
            layers.LSTM(128, return_sequences=True),
            layers.Dropout(0.3),
            
            layers.LSTM(64),
            layers.Dropout(0.3),
            
            # Dense layers for classification
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def prepare_data(self, X, y, test_size=0.2):
        """Prepare and reshape data for CNN-LSTM"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Reshape for CNN-LSTM (samples, timesteps, features)
        X_train_reshaped = X_train_scaled.reshape(X_train_scaled.shape[0], -1, 1)
        X_test_reshaped = X_test_scaled.reshape(X_test_scaled.shape[0], -1, 1)
        
        return X_train_reshaped, X_test_reshaped, y_train, y_test
    
    def train(self, X_train, y_train, X_val, y_val, epochs=50, batch_size=32):
        """Train the model"""
        if self.model is None:
            self.build_model()
        
        # Callbacks
        early_stop = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        checkpoint = ModelCheckpoint(
            'models/best_cnn_lstm_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            mode='max'
        )
        
        # Train
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stop, checkpoint],
            verbose=1
        )
        
        return self.history
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        
        print(f"\n{'='*50}")
        print(f"Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Test Loss: {loss:.4f}")
        print(f"{'='*50}")
        
        return accuracy, loss
    
    def predict(self, X):
        """Make predictions"""
        # Scale and reshape
        X_scaled = self.scaler.transform(X)
        X_reshaped = X_scaled.reshape(X_scaled.shape[0], -1, 1)
        
        # Predict
        predictions = self.model.predict(X_reshaped, verbose=0)
        predicted_classes = np.argmax(predictions, axis=1)
        
        return predicted_classes, predictions
    
    def save_model(self, model_dir='models'):
        """Save model and scaler"""
        os.makedirs(model_dir, exist_ok=True)
        
        # Save Keras model
        model_path = os.path.join(model_dir, 'cnn_lstm_model.h5')
        self.model.save(model_path)
        
        # Save scaler
        scaler_path = os.path.join(model_dir, 'cnn_lstm_scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        
        print(f"\nModel saved to: {model_path}")
        print(f"Scaler saved to: {scaler_path}")
    
    def load_model(self, model_dir='models'):
        """Load saved model and scaler"""
        model_path = os.path.join(model_dir, 'cnn_lstm_model.h5')
        scaler_path = os.path.join(model_dir, 'cnn_lstm_scaler.pkl')
        
        self.model = keras.models.load_model(model_path)
        self.scaler = joblib.load(scaler_path)
        
        print("Model and scaler loaded successfully!")


def train_cnn_lstm_model(dataset_path='datasets/seizure_dataset.csv'):
    """
    Complete training pipeline for CNN-LSTM model
    """
    if not TENSORFLOW_AVAILABLE:
        print("TensorFlow not available. Please install: pip install tensorflow")
        return
    
    print("Loading dataset...")
    df = pd.read_csv(dataset_path)
    
    # Prepare features and target
    if 'target' in df.columns:
        target_col = 'target'
    elif 'label' in df.columns:
        target_col = 'label'
    elif 'class' in df.columns:
        target_col = 'class'
    else:
        target_col = df.columns[-1]
    
    X = df.drop(columns=[target_col]).values
    y = df[target_col].values
    
    print(f"Dataset shape: {X.shape}")
    print(f"Classes: {np.unique(y)}")
    
    # Initialize model
    input_shape = (X.shape[1], 1)
    model = CNNLSTMSeizureModel(input_shape=input_shape, num_classes=len(np.unique(y)))
    
    # Prepare data
    X_train, X_test, y_train, y_test = model.prepare_data(X, y)
    
    print(f"\nTraining set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    
    # Build and train
    print("\nBuilding CNN-LSTM model...")
    model.build_model()
    model.model.summary()
    
    print("\nTraining model...")
    model.train(X_train, y_train, X_test, y_test, epochs=50, batch_size=32)
    
    # Evaluate
    print("\nEvaluating model...")
    accuracy, loss = model.evaluate(X_test, y_test)
    
    # Save
    model.save_model()
    
    print("\n✓ CNN-LSTM model training complete!")
    
    return model


if __name__ == "__main__":
    if TENSORFLOW_AVAILABLE:
        train_cnn_lstm_model()
    else:
        print("Please install TensorFlow to use CNN-LSTM model:")
        print("pip install tensorflow")
