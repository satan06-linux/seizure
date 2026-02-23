"""
Flask Backend API for SeizureGuard AI
RESTful API endpoints for all AI functionalities
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from modules.predictor import SeizurePredictor
from modules.symptom_checker import SymptomChecker
from modules.chatbot import SeizureChatbot
from modules.doctor_recommender import DoctorRecommender
from modules.file_processor import FileProcessor

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize modules
try:
    predictor = SeizurePredictor()
    predictor_loaded = True
except:
    predictor_loaded = False

symptom_checker = SymptomChecker()
chatbot = SeizureChatbot()
doctor_recommender = DoctorRecommender()
file_processor = FileProcessor()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'predictor_loaded': predictor_loaded,
        'version': '1.0.0'
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict seizure from features"""
    try:
        if not predictor_loaded:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please train the model first.'
            }), 500
        
        data = request.json
        features = data.get('features', {})
        
        result = predictor.predict(features)
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Process uploaded file"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Save file temporarily
        temp_path = f"temp_{file.filename}"
        file.save(temp_path)
        
        # Process file
        result = file_processor.process_file(temp_path)
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        if result['success']:
            # Make prediction if model is loaded
            if predictor_loaded:
                prediction = predictor.predict(result['features'])
                result['prediction'] = prediction
            
            return jsonify({
                'success': True,
                'result': result
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error')
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/symptoms/analyze', methods=['POST'])
def analyze_symptoms():
    """Analyze symptoms"""
    try:
        data = request.json
        symptom_text = data.get('symptoms', '')
        
        if not symptom_text:
            return jsonify({
                'success': False,
                'error': 'No symptoms provided'
            }), 400
        
        result = symptom_checker.analyze_symptoms(symptom_text)
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with AI assistant"""
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            }), 400
        
        response = chatbot.chat(message)
        
        return jsonify({
            'success': True,
            'response': response
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """Get doctor recommendations"""
    try:
        location = request.args.get('location')
        specialization = request.args.get('specialization')
        emergency = request.args.get('emergency', 'false').lower() == 'true'
        risk_level = request.args.get('risk_level')
        top_n = int(request.args.get('top_n', 5))
        
        doctors = doctor_recommender.recommend_doctors(
            risk_level=risk_level,
            location=location,
            specialization=specialization,
            emergency=emergency,
            top_n=top_n
        )
        
        return jsonify({
            'success': True,
            'doctors': doctors
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/doctors/locations', methods=['GET'])
def get_locations():
    """Get all available locations"""
    try:
        locations = doctor_recommender.get_all_locations()
        return jsonify({
            'success': True,
            'locations': locations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/doctors/specializations', methods=['GET'])
def get_specializations():
    """Get all specializations"""
    try:
        specializations = doctor_recommender.get_all_specializations()
        return jsonify({
            'success': True,
            'specializations': specializations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
