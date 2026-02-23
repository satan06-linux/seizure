# 🏗️ System Architecture

## Overview

SeizureGuard AI follows a modular, layered architecture designed for maintainability, scalability, and ease of use.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                     │
│                    (Streamlit Frontend)                      │
├─────────────────────────────────────────────────────────────┤
│  Home  │  Upload  │  Symptom  │  Chatbot  │  Find Doctor   │
│  Page  │   EEG    │  Checker  │           │                │
└────┬────────┬──────────┬─────────┬──────────────┬───────────┘
     │        │          │         │              │
     ▼        ▼          ▼         ▼              ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│                      (app.py)                                │
├─────────────────────────────────────────────────────────────┤
│  • Session Management                                        │
│  • Page Routing                                              │
│  • UI Components                                             │
│  • Result Visualization                                      │
└────┬────────┬──────────┬─────────┬──────────────┬───────────┘
     │        │          │         │              │
     ▼        ▼          ▼         ▼              ▼
┌─────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                      │
│                      (modules/)                              │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  Predictor   │   Symptom    │   Chatbot    │    Doctor      │
│              │   Checker    │              │  Recommender   │
├──────────────┼──────────────┴──────────────┴────────────────┤
│ File Processor                                               │
├──────────────────────────────────────────────────────────────┤
│ Trainer                                                      │
└────┬────────┬──────────┬─────────┬──────────────┬───────────┘
     │        │          │         │              │
     ▼        ▼          ▼         ▼              ▼
┌─────────────────────────────────────────────────────────────┐
│                    UTILITY LAYER                             │
│                      (utils/)                                │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ PDF Reader   │ Image Reader │  EDF Reader  │   (Future)     │
└──────────────┴──────────────┴──────────────┴────────────────┘
     │        │          │
     ▼        ▼          ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   Models     │   Datasets   │    Temp      │   (Future DB)  │
│   (.pkl)     │    (.csv)    │   Files      │                │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

## Component Details

### 1. User Interface Layer (Streamlit)

**Purpose**: Provide intuitive web interface for users

**Components**:
- Home Page: Overview and features
- Upload EEG: File upload and analysis
- Symptom Checker: Text input and analysis
- Chatbot: Interactive Q&A
- Find Doctor: Search and recommendations

**Technologies**: Streamlit, Plotly, Custom CSS

### 2. Application Layer (app.py)

**Purpose**: Orchestrate UI and business logic

**Responsibilities**:
- Page routing and navigation
- Session state management
- User input handling
- Result visualization
- Error handling

**Key Functions**:
- `home_page()`: Display home
- `upload_file_page()`: Handle file uploads
- `symptom_checker_page()`: Symptom analysis UI
- `chatbot_page()`: Chat interface
- `find_neurologist_page()`: Doctor search UI

### 3. Business Logic Layer (modules/)

#### 3.1 Predictor Module

**Purpose**: Make seizure predictions

**Input**: Feature dictionary/DataFrame
**Output**: Prediction, confidence, risk level
**Dependencies**: joblib, scikit-learn

**Flow**:
```
Features → Prepare Input → Scale → Predict → Format Result
```

#### 3.2 Symptom Checker Module

**Purpose**: Analyze text symptoms

**Input**: Symptom text string
**Output**: Risk assessment, recommendations
**Dependencies**: None (rule-based)

**Flow**:
```
Text → Detect Symptoms → Calculate Risk → Identify Condition → Generate Recommendations
```

#### 3.3 Chatbot Module

**Purpose**: Answer seizure-related questions

**Input**: User question
**Output**: Intelligent response
**Dependencies**: None (pattern matching)

**Flow**:
```
Question → Pattern Match → Intent Detection → Generate Response
```

#### 3.4 Doctor Recommender Module

**Purpose**: Find neurologists

**Input**: Search criteria (location, specialization, etc.)
**Output**: List of doctors
**Dependencies**: pandas

**Flow**:
```
Criteria → Filter Database → Rank → Format Results
```

#### 3.5 File Processor Module

**Purpose**: Process multiple file formats

**Input**: File path
**Output**: Extracted features
**Dependencies**: pandas, pdfplumber, pytesseract, mne

**Flow**:
```
File → Detect Type → Extract Data → Convert to Features
```

#### 3.6 Trainer Module

**Purpose**: Train ML models

**Input**: Dataset CSV
**Output**: Trained model files
**Dependencies**: scikit-learn, joblib

**Flow**:
```
Load Data → Prepare Features → Split → Train → Evaluate → Save
```

### 4. Utility Layer (utils/)

**Purpose**: Provide reusable helper functions

**Components**:
- `pdf_reader.py`: PDF text extraction
- `image_reader.py`: OCR processing
- `edf_reader.py`: EEG file reading

### 5. Data Layer

**Purpose**: Store models, datasets, and temporary files

**Components**:
- `models/`: Trained model files (.pkl)
- `datasets/`: Training data (.csv)
- `temp/`: Temporary uploaded files

## Data Flow

### Prediction Flow

```
User Upload File
    ↓
File Processor (detect type, extract features)
    ↓
Predictor (load model, make prediction)
    ↓
Result Formatting (confidence, risk level, explanation)
    ↓
UI Display (metrics, charts, recommendations)
    ↓
Doctor Recommender (based on risk level)
    ↓
Display Doctor List
```

### Symptom Analysis Flow

```
User Enter Symptoms
    ↓
Symptom Checker (keyword matching)
    ↓
Risk Calculation (weighted scoring)
    ↓
Condition Identification
    ↓
Recommendation Generation
    ↓
UI Display (risk level, advice)
    ↓
Doctor Recommender (if needed)
```

### Chat Flow

```
User Ask Question
    ↓
Chatbot (pattern matching)
    ↓
Intent Detection
    ↓
Response Generation (from knowledge base)
    ↓
Display Response
    ↓
Store in History
```

## Design Patterns

### 1. Modular Design
- Each module has single responsibility
- Loose coupling between components
- Easy to test and maintain

### 2. Separation of Concerns
- UI logic separate from business logic
- Data processing separate from ML
- Clear layer boundaries

### 3. Factory Pattern
- File processor creates appropriate handler
- Chatbot selects response handler

### 4. Strategy Pattern
- Different file processing strategies
- Multiple prediction models (RF, CNN-LSTM)

## Technology Stack

### Frontend
- **Streamlit**: Web framework
- **Plotly**: Interactive charts
- **CSS**: Custom styling

### Backend
- **Python 3.11**: Core language
- **scikit-learn**: Machine learning
- **pandas**: Data manipulation
- **numpy**: Numerical computing

### File Processing
- **pdfplumber**: PDF extraction
- **pytesseract**: OCR
- **opencv**: Image processing
- **mne**: EEG data

### Model Persistence
- **joblib**: Model serialization
- **pickle**: Object serialization

## Scalability Considerations

### Current Architecture
- Single-server deployment
- In-memory processing
- File-based storage

### Future Enhancements
- Database integration (PostgreSQL)
- Caching layer (Redis)
- API layer (FastAPI)
- Microservices architecture
- Load balancing
- Cloud storage (S3)

## Security Architecture

### Current Implementation
- Local processing only
- No external API calls
- Temporary file cleanup
- No permanent storage

### Future Enhancements
- User authentication (OAuth)
- Role-based access control
- Data encryption
- HIPAA compliance
- Audit logging

## Performance Optimization

### Current Optimizations
- Model caching in session state
- Efficient data structures
- Vectorized operations (numpy)
- Lazy loading

### Future Optimizations
- Model quantization
- Batch processing
- Async operations
- CDN for static assets
- Database indexing

## Error Handling

### Strategy
- Try-catch blocks at each layer
- Graceful degradation
- User-friendly error messages
- Logging for debugging

### Error Flow
```
Error Occurs
    ↓
Catch at Module Level
    ↓
Log Error Details
    ↓
Return Error Result
    ↓
Display User-Friendly Message
    ↓
Suggest Resolution
```

## Testing Architecture

### Unit Tests
- Each module independently testable
- Mock external dependencies
- Test edge cases

### Integration Tests
- Test module interactions
- End-to-end workflows
- File processing pipelines

### System Tests
- Full application testing
- UI interaction testing
- Performance testing

## Deployment Architecture

### Development
```
Local Machine → Python Virtual Env → Streamlit Dev Server
```

### Production (Streamlit Cloud)
```
GitHub Repo → Streamlit Cloud → Public URL
```

### Production (Self-Hosted)
```
Server → Docker Container → Nginx Reverse Proxy → Public IP
```

## Monitoring & Logging

### Current
- Console logging
- Error messages in UI

### Future
- Application logs (logging module)
- Performance metrics
- User analytics
- Error tracking (Sentry)
- Health checks

## Conclusion

The architecture is designed to be:
- **Modular**: Easy to modify individual components
- **Scalable**: Can grow with requirements
- **Maintainable**: Clear structure and documentation
- **Testable**: Each layer independently testable
- **Extensible**: Easy to add new features

This foundation supports current needs while allowing for future growth.
