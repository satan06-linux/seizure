"""
Generate Sample Seizure Dataset
This script creates a synthetic dataset for testing purposes
"""
import pandas as pd
import numpy as np
import os

def generate_sample_dataset(n_samples=1000, n_features=20, output_path='datasets/seizure_dataset.csv'):
    """
    Generate synthetic seizure dataset
    
    Args:
        n_samples: Number of samples to generate
        n_features: Number of features per sample
        output_path: Path to save the dataset
    """
    print(f"Generating sample dataset with {n_samples} samples and {n_features} features...")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Generate features for each class
    samples_per_class = n_samples // 3
    
    # Class 0: Normal (low variance, centered around 0)
    normal_data = np.random.randn(samples_per_class, n_features) * 0.5
    normal_labels = np.zeros(samples_per_class)
    
    # Class 1: Preictal (medium variance, slightly elevated)
    preictal_data = np.random.randn(samples_per_class, n_features) * 1.0 + 0.5
    preictal_labels = np.ones(samples_per_class)
    
    # Class 2: Seizure (high variance, elevated)
    seizure_data = np.random.randn(samples_per_class, n_features) * 1.5 + 1.0
    seizure_labels = np.full(samples_per_class, 2)
    
    # Combine all data
    X = np.vstack([normal_data, preictal_data, seizure_data])
    y = np.concatenate([normal_labels, preictal_labels, seizure_labels])
    
    # Shuffle the data
    indices = np.random.permutation(len(X))
    X = X[indices]
    y = y[indices]
    
    # Create DataFrame
    feature_names = [f'feature_{i+1}' for i in range(n_features)]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y.astype(int)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    print(f"✓ Dataset saved to: {output_path}")
    print(f"✓ Shape: {df.shape}")
    print(f"✓ Class distribution:")
    print(df['target'].value_counts().sort_index())
    print(f"\nFirst few rows:")
    print(df.head())
    
    return df


if __name__ == "__main__":
    # Generate dataset
    df = generate_sample_dataset(
        n_samples=1000,
        n_features=20,
        output_path='datasets/seizure_dataset.csv'
    )
    
    print("\n" + "="*60)
    print("Sample dataset generated successfully!")
    print("="*60)
    print("\nNext steps:")
    print("1. Train the model: python modules/trainer.py")
    print("2. Run the app: streamlit run app.py")
