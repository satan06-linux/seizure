# 🧠 SeizureGuard AI

<div align="center">

**Intelligent Seizure Detection and Neurologist Recommendation System**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()
[![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-FF4B4B.svg)](https://streamlit.io)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-ready AI-powered web application that detects epileptic seizures using EEG datasets, user symptoms, uploaded files, and chatbot interaction.

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📸 Screenshots

<div align="center">

### Home Page
*Beautiful, intuitive interface with clear navigation*

### Upload & Analyze
*Multi-format file support with instant predictions*

### AI Chatbot
*Intelligent assistant for seizure-related questions*

</div>

## 🌟 Features

### Multi-Input Support
- **EEG CSV Dataset Upload**: Process tabular EEG data
- **EEG Report PDF Upload**: Extract data from PDF reports
- **EEG Image Upload**: OCR-based text extraction from scanned reports
- **EDF File Support**: Standard EEG data format processing
- **Symptom Text Input**: Natural language symptom analysis
- **Chat Conversation**: Interactive AI assistant

### Core Capabilities
- ✅ Seizure risk prediction (Normal, Preictal, Seizure)
- ✅ Confidence scoring and probability distribution
- ✅ Risk level assessment (LOW, MEDIUM, HIGH)
- ✅ Intelligent symptom analysis
- ✅ Personalized recommendations
- ✅ Neurologist finder with specialization matching
- ✅ AI chatbot for seizure-related queries

## 📁 Project Structure

```
seizureguard_ai/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── SETUP_GUIDE.md                 # Detailed setup instructions
│
├── models/                         # Trained models (generated after training)
│   ├── seizure_model.pkl
│   ├── scaler.pkl
│   └── feature_columns.pkl
│
├── datasets/                       # Data files
│   ├── seizure_dataset.csv        # Training dataset (user-provided)
│   └── neurologists.csv           # Doctor database (auto-generated)
│
├── modules/                        # Core modules
│   ├── __init__.py
│   ├── trainer.py                 # Model training
│   ├── predictor.py               # Prediction engine
│   ├── file_processor.py          # Multi-format file processing
│   ├── symptom_checker.py         # Symptom analysis
│   ├── chatbot.py                 # AI chatbot
│   └── doctor_recommender.py      # Neurologist recommendations
│
└── utils/                          # Utility functions
    ├── __init__.py
    ├── pdf_reader.py              # PDF processing
    ├── image_reader.py            # OCR for images
    └── edf_reader.py              # EDF file handling
```

## 🎥 Demo

Try the live demo: [Coming Soon - Deploy to Streamlit Cloud]

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip package manager
- 4GB RAM minimum

### Installation

1. **Navigate to project directory**
```bash
cd temp/seizureguard_ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Prepare your dataset**
   - Place your seizure dataset CSV in `datasets/seizure_dataset.csv`
   - Dataset should have features in columns and a target column (label/class)

4. **Train the model**
```bash
python modules/trainer.py
```

5. **Run the application**
```bash
streamlit run app.py
```

6. **Open browser**
   - The app will automatically open at `http://localhost:8501`

## 📊 Dataset Requirements

Your `seizure_dataset.csv` should have:
- Multiple feature columns (EEG channel data, statistical features, etc.)
- One target column named: `target`, `label`, or `class`
- Target values should be: 0 (Normal), 1 (Preictal), 2 (Seizure)

Example structure:
```csv
feature_1,feature_2,feature_3,...,target
0.123,0.456,0.789,...,0
0.234,0.567,0.890,...,1
0.345,0.678,0.901,...,2
```

## 🎯 Usage Guide

### 1. Upload EEG File
- Navigate to "Upload EEG File" page
- Upload CSV, PDF, Image, or EDF file
- Click "Analyze for Seizure Detection"
- View prediction results and doctor recommendations

### 2. Symptom Checker
- Navigate to "Symptom Checker" page
- Describe your symptoms in natural language
- Get risk assessment and recommendations
- View detected symptoms and urgency level

### 3. AI Chatbot
- Navigate to "Chatbot" page
- Ask questions about seizures, epilepsy, treatment, etc.
- Get instant, intelligent responses
- Use quick question buttons for common queries

### 4. Find Neurologist
- Navigate to "Find Neurologist" page
- Filter by location, specialization, emergency availability
- View doctor profiles with ratings and contact info
- Get emergency neurologist contacts

## 🔧 Module Details

### Trainer (`modules/trainer.py`)
- Loads and preprocesses dataset
- Trains RandomForest classifier
- Evaluates model performance
- Saves trained model, scaler, and feature columns

### Predictor (`modules/predictor.py`)
- Loads trained model
- Accepts feature input (dict, DataFrame, or array)
- Returns prediction, confidence, risk level, and explanation
- Handles missing features gracefully

### File Processor (`modules/file_processor.py`)
- Auto-detects file type
- Processes CSV, PDF, Image, EDF formats
- Extracts numerical features
- Returns structured result with features

### Symptom Checker (`modules/symptom_checker.py`)
- Analyzes symptom text using keyword matching
- Calculates risk score (0-100)
- Identifies possible condition
- Generates personalized recommendations

### Chatbot (`modules/chatbot.py`)
- Rule-based NLP for seizure-related queries
- Pattern matching for intent detection
- Comprehensive knowledge base
- Conversation history tracking

### Doctor Recommender (`modules/doctor_recommender.py`)
- Maintains neurologist database
- Filters by location, specialization, emergency availability
- Ranks by rating and experience
- Returns formatted recommendations

## 🎨 Streamlit Interface

### Pages
1. **Home**: Overview, features, system capabilities
2. **Upload EEG File**: File upload and analysis
3. **Symptom Checker**: Text-based symptom analysis
4. **Chatbot**: Interactive AI assistant
5. **Find Neurologist**: Doctor search and recommendations

### Features
- Responsive design
- Custom CSS styling
- Risk-level color coding (Red/Orange/Green)
- Interactive charts (Plotly)
- Real-time predictions
- Session state management

## 🔒 Security & Privacy

- No data is stored permanently
- Temporary files are deleted after processing
- All processing happens locally
- No external API calls for predictions

## ⚠️ Disclaimer

**This is an AI assistant tool for educational and informational purposes only.**

- Not a substitute for professional medical advice
- Always consult qualified healthcare professionals
- In case of emergency, call 911 immediately
- Do not rely solely on AI predictions for medical decisions

## 🛠️ Troubleshooting

### Model not found error
```bash
# Train the model first
python modules/trainer.py
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Tesseract OCR error
```bash
# Install Tesseract OCR
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# Linux: sudo apt-get install tesseract-ocr
# Mac: brew install tesseract
```

### MNE library error (for EDF files)
```bash
# Ensure MNE is installed
pip install mne
```

## 📈 Future Enhancements

- [ ] Deep learning models (CNN + LSTM)
- [ ] Real-time EEG streaming
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Cloud deployment
- [ ] User authentication
- [ ] Medical record integration
- [ ] Telemedicine integration

## 👥 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational purposes. Consult legal requirements for medical software in your jurisdiction.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/seizureguard-ai&type=Date)](https://star-history.com/#YOUR_USERNAME/seizureguard-ai&Date)

## 📊 Project Stats

![GitHub repo size](https://img.shields.io/github/repo-size/YOUR_USERNAME/seizureguard-ai)
![GitHub code size](https://img.shields.io/github/languages/code-size/YOUR_USERNAME/seizureguard-ai)
![Lines of code](https://img.shields.io/tokei/lines/github/YOUR_USERNAME/seizureguard-ai)

## 📞 Support

For issues, questions, or suggestions:
- 🐛 [Open an issue](https://github.com/YOUR_USERNAME/seizureguard-ai/issues)
- 💬 [Start a discussion](https://github.com/YOUR_USERNAME/seizureguard-ai/discussions)
- ⭐ Star this repo if you find it helpful!

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io), [scikit-learn](https://scikit-learn.org), and Python
- EEG processing powered by [MNE-Python](https://mne.tools)
- OCR powered by [Tesseract](https://github.com/tesseract-ocr/tesseract)

## 📜 Citation

If you use this project in your research, please cite:

```bibtex
@software{seizureguard_ai,
  title = {SeizureGuard AI: Intelligent Seizure Detection System},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/YOUR_USERNAME/seizureguard-ai}
}
```

## 🔗 Links

- [Documentation](https://github.com/YOUR_USERNAME/seizureguard-ai/wiki)
- [Live Demo](https://YOUR_USERNAME-seizureguard-ai.streamlit.app)
- [Report Bug](https://github.com/YOUR_USERNAME/seizureguard-ai/issues)
- [Request Feature](https://github.com/YOUR_USERNAME/seizureguard-ai/issues)

---

<div align="center">

**Made with ❤️ for better neurological healthcare**

⭐ Star us on GitHub — it motivates us a lot!

[⬆ Back to Top](#-seizureguard-ai)

</div>
