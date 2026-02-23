# 🔌 API Documentation

## Module APIs

### 1. Predictor API

```python
from modules.predictor import SeizurePredictor

# Initialize
predictor = SeizurePredictor()

# Make prediction
features = {'feature_1': 0.5, 'feature_2': 0.3, ...}
result = predictor.predict(features)

# Result structure
{
    'prediction': 'SEIZURE',
    'confidence': 85.5,
    'risk_level': 'HIGH',
    'probabilities': {
        'NORMAL': 5.2,
        'PREICTAL': 9.3,
        'SEIZURE': 85.5
    },
    'explanation': 'Seizure activity detected...'
}
```

### 2. Symptom Checker API

```python
from modules.symptom_checker import SymptomChecker

checker = SymptomChecker()
result = checker.analyze_symptoms("I feel dizzy and confused")

# Result structure
{
    'detected_symptoms': [...],
    'risk_score': 45.5,
    'risk_level': 'MEDIUM',
    'possible_condition': 'PREICTAL',
    'recommendations': [...],
    'urgency': 'URGENT'
}
```

### 3. Chatbot API

```python
from modules.chatbot import SeizureChatbot

bot = SeizureChatbot()
response = bot.chat("What is a seizure?")

# Response structure
{
    'message': 'A seizure is...',
    'intent': 'respond_seizure_info',
    'confidence': 0.85
}
```

### 4. Doctor Recommender API

```python
from modules.doctor_recommender import DoctorRecommender

recommender = DoctorRecommender()
doctors = recommender.recommend_doctors(
    location='California',
    emergency=True,
    top_n=5
)

# Returns list of doctor dictionaries
```

### 5. File Processor API

```python
from modules.file_processor import FileProcessor

processor = FileProcessor()
result = processor.process_file('path/to/file.csv')

# Result structure
{
    'success': True,
    'file_type': 'csv',
    'features': {...},
    'message': 'Successfully processed...'
}
```
