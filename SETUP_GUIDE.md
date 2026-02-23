# 📘 SeizureGuard AI - Complete Setup Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Dataset Preparation](#dataset-preparation)
4. [Model Training](#model-training)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.11 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 2 GB free space
- **Internet**: Required for initial package installation

### Software Dependencies
- Python 3.11+
- pip (Python package manager)
- Tesseract OCR (for image processing)

## Installation Steps

### Step 1: Install Python

**Windows:**
1. Download Python 3.11+ from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

**macOS:**
```bash
brew install python@3.11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3-pip
```

### Step 2: Install Tesseract OCR (for Image Processing)

**Windows:**
1. Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run installer
3. Add to PATH: `C:\Program Files\Tesseract-OCR`

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt install tesseract-ocr
```

### Step 3: Clone/Download Project

```bash
cd temp/seizureguard_ai
```

### Step 4: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- streamlit (Web framework)
- pandas, numpy (Data processing)
- scikit-learn (Machine learning)
- matplotlib, plotly (Visualization)
- pdfplumber (PDF processing)
- pytesseract (OCR)
- opencv-python (Image processing)
- mne (EEG data processing)
- beautifulsoup4 (Web scraping)
- joblib (Model serialization)

**Installation time**: 5-10 minutes depending on internet speed

## Dataset Preparation

### Option 1: Use Your Own Dataset

1. **Prepare your CSV file** with EEG features
   - Features should be in columns
   - Include a target column: `target`, `label`, or `class`
   - Target values: 0 (Normal), 1 (Preictal), 2 (Seizure)

2. **Save as**: `datasets/seizure_dataset.csv`

Example format:
```csv
mean_ch1,std_ch1,max_ch1,min_ch1,...,target
0.123,0.456,0.789,0.012,...,0
0.234,0.567,0.890,0.023,...,1
0.345,0.678,0.901,0.034,...,2
```

### Option 2: Use Public Dataset

**Recommended: CHB-MIT Scalp EEG Database**

1. Download from [PhysioNet](https://physionet.org/content/chbmit/1.0.0/)
2. Extract features using provided notebooks
3. Save as `datasets/seizure_dataset.csv`

**Alternative: Bonn University EEG Dataset**

1. Download from [Bonn University](http://epileptologie-bonn.de/cms/front_content.php?idcat=193&lang=3)
2. Process and format as CSV
3. Save in datasets folder

### Dataset Requirements

- **Minimum rows**: 100 (1000+ recommended)
- **Features**: 10+ columns
- **Target column**: Required
- **Missing values**: Should be handled (filled or removed)
- **Format**: CSV with headers

## Model Training

### Step 1: Verify Dataset

```bash
# Check if dataset exists
ls datasets/seizure_dataset.csv

# View first few rows (optional)
head datasets/seizure_dataset.csv
```

### Step 2: Train the Model

```bash
python modules/trainer.py
```

**Expected output:**
```
Loading dataset...
Dataset shape: (1000, 50)
Columns: ['feature_1', 'feature_2', ..., 'target']

Features: 49
Target distribution:
0    400
1    300
2    300

Train size: 800, Test size: 200

Training RandomForest model...
Model training complete!

==================================================
Model Accuracy: 0.9500 (95.00%)
==================================================

Classification Report:
              precision    recall  f1-score   support
           0       0.95      0.96      0.96        80
           1       0.94      0.93      0.94        60
           2       0.96      0.95      0.95        60

Model saved to: models/seizure_model.pkl
Scaler saved to: models/scaler.pkl
Features saved to: models/feature_columns.pkl
```

### Step 3: Verify Model Files

```bash
ls models/
# Should show:
# seizure_model.pkl
# scaler.pkl
# feature_columns.pkl
```

## Running the Application

### Step 1: Start Streamlit Server

```bash
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.x:8501
```

### Step 2: Open Browser

- Automatically opens at `http://localhost:8501`
- Or manually navigate to the URL shown

### Step 3: Navigate the App

1. **Home Page**: Overview and features
2. **Upload EEG File**: Test with sample files
3. **Symptom Checker**: Enter symptoms
4. **Chatbot**: Ask questions
5. **Find Neurologist**: Search doctors

## Testing

### Test 1: File Upload

1. Navigate to "Upload EEG File"
2. Upload a CSV file with EEG data
3. Click "Analyze for Seizure Detection"
4. Verify prediction results appear

### Test 2: Symptom Checker

1. Navigate to "Symptom Checker"
2. Enter: "I feel dizziness and confusion"
3. Click "Analyze Symptoms"
4. Verify risk assessment appears

### Test 3: Chatbot

1. Navigate to "Chatbot"
2. Type: "What is a seizure?"
3. Verify intelligent response
4. Try other questions

### Test 4: Doctor Finder

1. Navigate to "Find Neurologist"
2. Select filters (location, specialization)
3. Click "Search"
4. Verify doctor list appears

## Troubleshooting

### Issue 1: Module Import Errors

**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

### Issue 2: Model Not Found

**Error**: `FileNotFoundError: Model files not found`

**Solution**:
```bash
# Train the model first
python modules/trainer.py
```

### Issue 3: Tesseract Not Found

**Error**: `TesseractNotFoundError`

**Solution**:
- Install Tesseract OCR (see Step 2)
- Add to system PATH
- Restart terminal

**Windows specific**:
```python
# Add to image_reader.py if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Issue 4: Port Already in Use

**Error**: `Port 8501 is already in use`

**Solution**:
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Issue 5: Dataset Format Error

**Error**: `KeyError: 'target'`

**Solution**:
- Ensure dataset has a target column
- Rename column to 'target', 'label', or 'class'
- Check CSV format and headers

### Issue 6: Memory Error

**Error**: `MemoryError` during training

**Solution**:
- Reduce dataset size
- Use fewer features
- Increase system RAM
- Close other applications

### Issue 7: Streamlit Won't Start

**Solution**:
```bash
# Clear Streamlit cache
streamlit cache clear

# Reinstall Streamlit
pip uninstall streamlit
pip install streamlit
```

## Advanced Configuration

### Change Model Parameters

Edit `modules/trainer.py`:
```python
self.model = RandomForestClassifier(
    n_estimators=200,  # Increase for better accuracy
    max_depth=15,      # Adjust depth
    random_state=42,
    n_jobs=-1
)
```

### Customize Doctor Database

Edit `modules/doctor_recommender.py`:
- Add more doctors to `create_sample_database()`
- Or create `datasets/neurologists.csv`

### Modify UI Theme

Edit `app.py` CSS section:
```python
st.markdown("""
<style>
    .main-header {
        color: #your-color;
    }
</style>
""", unsafe_allow_html=True)
```

## Performance Optimization

### For Large Datasets

1. **Use sampling**:
```python
df = df.sample(n=10000, random_state=42)
```

2. **Feature selection**:
```python
from sklearn.feature_selection import SelectKBest
selector = SelectKBest(k=20)
X_selected = selector.fit_transform(X, y)
```

3. **Model optimization**:
```python
# Use fewer trees
n_estimators=50
```

### For Faster Predictions

1. **Cache model loading**:
```python
@st.cache_resource
def load_model():
    return SeizurePredictor()
```

2. **Reduce file processing**:
- Limit image resolution
- Sample EDF data

## Deployment (Optional)

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy

### Deploy to Heroku

1. Create `Procfile`:
```
web: streamlit run app.py --server.port $PORT
```

2. Deploy:
```bash
heroku create seizureguard-ai
git push heroku main
```

## Next Steps

1. ✅ Test all features thoroughly
2. ✅ Customize doctor database
3. ✅ Add your own branding
4. ✅ Improve model with more data
5. ✅ Deploy to production

## Support

If you encounter issues:
1. Check this guide
2. Review error messages
3. Check Python version: `python --version`
4. Check package versions: `pip list`
5. Search for similar issues online

## Conclusion

You now have a fully functional SeizureGuard AI system! 

**Remember**: This is an educational tool. Always consult healthcare professionals for medical advice.

---

**Happy coding! 🧠💻**
