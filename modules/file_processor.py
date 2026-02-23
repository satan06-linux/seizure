"""
Module 3: File Processor
Processes different file types (CSV, PDF, Image, EDF) and extracts features
"""
import pandas as pd
import numpy as np
import pdfplumber
import pytesseract
from PIL import Image
import cv2
import os
import re


class FileProcessor:
    def __init__(self):
        self.supported_formats = ['csv', 'pdf', 'png', 'jpg', 'jpeg', 'edf']
    
    def detect_file_type(self, file_path):
        """Detect file type from extension"""
        ext = os.path.splitext(file_path)[1].lower().replace('.', '')
        return ext if ext in self.supported_formats else None
    
    def process_file(self, file_path):
        """Main method to process any supported file type"""
        file_type = self.detect_file_type(file_path)
        
        if file_type is None:
            raise ValueError(f"Unsupported file format. Supported: {self.supported_formats}")
        
        print(f"Processing {file_type.upper()} file...")
        
        if file_type == 'csv':
            return self.process_csv(file_path)
        elif file_type == 'pdf':
            return self.process_pdf(file_path)
        elif file_type in ['png', 'jpg', 'jpeg']:
            return self.process_image(file_path)
        elif file_type == 'edf':
            return self.process_edf(file_path)
    
    def process_csv(self, file_path):
        """Process CSV file containing EEG data"""
        try:
            df = pd.read_csv(file_path)
            print(f"CSV loaded: {df.shape}")
            
            # Extract features from CSV
            # Assume CSV contains EEG channel data
            features = self.extract_features_from_dataframe(df)
            
            return {
                'success': True,
                'file_type': 'csv',
                'features': features,
                'raw_data': df,
                'message': f"Successfully processed CSV with {len(df)} rows"
            }
            
        except Exception as e:
            return {
                'success': False,
                'file_type': 'csv',
                'error': str(e)
            }
    
    def process_pdf(self, file_path):
        """Process PDF file and extract text"""
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            
            print(f"PDF text extracted: {len(text)} characters")
            
            # Extract numerical features from text
            features = self.extract_features_from_text(text)
            
            return {
                'success': True,
                'file_type': 'pdf',
                'features': features,
                'text': text,
                'message': f"Successfully extracted text from PDF ({len(text)} chars)"
            }
            
        except Exception as e:
            return {
                'success': False,
                'file_type': 'pdf',
                'error': str(e)
            }
    
    def process_image(self, file_path):
        """Process image file using OCR"""
        try:
            # Read image
            image = Image.open(file_path)
            
            # Extract text using OCR
            text = pytesseract.image_to_string(image)
            print(f"Image OCR extracted: {len(text)} characters")
            
            # Also analyze image properties
            img_array = np.array(image)
            
            # Extract features
            features = self.extract_features_from_text(text)
            
            return {
                'success': True,
                'file_type': 'image',
                'features': features,
                'text': text,
                'image_shape': img_array.shape,
                'message': f"Successfully processed image and extracted text"
            }
            
        except Exception as e:
            return {
                'success': False,
                'file_type': 'image',
                'error': str(e)
            }
    
    def process_edf(self, file_path):
        """Process EDF file (EEG data format)"""
        try:
            import mne
            
            # Read EDF file
            raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
            
            # Get data
            data = raw.get_data()
            sfreq = raw.info['sfreq']
            
            print(f"EDF loaded: {data.shape} at {sfreq} Hz")
            
            # Extract features from EEG signals
            features = self.extract_features_from_eeg(data, sfreq)
            
            return {
                'success': True,
                'file_type': 'edf',
                'features': features,
                'channels': raw.ch_names,
                'sampling_rate': sfreq,
                'message': f"Successfully processed EDF with {len(raw.ch_names)} channels"
            }
            
        except Exception as e:
            return {
                'success': False,
                'file_type': 'edf',
                'error': str(e)
            }
    
    def extract_features_from_dataframe(self, df):
        """Extract statistical features from DataFrame"""
        features = {}
        
        # Get numeric columns only
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            # No numeric data, create dummy features
            return self.create_dummy_features()
        
        # Calculate statistics for each column
        for col in numeric_cols[:20]:  # Limit to first 20 columns
            features[f'{col}_mean'] = df[col].mean()
            features[f'{col}_std'] = df[col].std()
            features[f'{col}_max'] = df[col].max()
            features[f'{col}_min'] = df[col].min()
        
        return features
    
    def extract_features_from_text(self, text):
        """Extract features from text (PDF/Image OCR)"""
        # Extract numbers from text
        numbers = re.findall(r'-?\d+\.?\d*', text)
        numbers = [float(n) for n in numbers if n]
        
        if len(numbers) == 0:
            return self.create_dummy_features()
        
        # Create statistical features
        features = {
            'text_mean': np.mean(numbers),
            'text_std': np.std(numbers),
            'text_max': np.max(numbers),
            'text_min': np.min(numbers),
            'text_count': len(numbers)
        }
        
        # Pad with additional features
        for i in range(min(len(numbers), 15)):
            features[f'value_{i}'] = numbers[i]
        
        return features
    
    def extract_features_from_eeg(self, data, sfreq):
        """Extract features from EEG signal data"""
        features = {}
        
        # Calculate features for each channel
        for i, channel_data in enumerate(data[:8]):  # First 8 channels
            features[f'ch{i}_mean'] = np.mean(channel_data)
            features[f'ch{i}_std'] = np.std(channel_data)
            features[f'ch{i}_max'] = np.max(channel_data)
            features[f'ch{i}_min'] = np.min(channel_data)
            features[f'ch{i}_energy'] = np.sum(channel_data ** 2)
        
        return features
    
    def create_dummy_features(self, n_features=20):
        """Create dummy features when extraction fails"""
        return {f'feature_{i}': 0.0 for i in range(n_features)}


if __name__ == "__main__":
    processor = FileProcessor()
    
    # Test with a sample file
    print("File Processor initialized successfully!")
    print(f"Supported formats: {processor.supported_formats}")
