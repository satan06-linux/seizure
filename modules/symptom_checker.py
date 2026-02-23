"""
Module 4: Symptom Checker
Analyzes user symptoms and provides risk assessment
"""
import re
from typing import Dict, List, Tuple


class SymptomChecker:
    def __init__(self):
        # Define symptom keywords and their severity weights
        self.symptom_keywords = {
            # High severity symptoms
            'seizure': {'weight': 10, 'severity': 'high'},
            'convulsion': {'weight': 10, 'severity': 'high'},
            'unconscious': {'weight': 10, 'severity': 'high'},
            'collapse': {'weight': 9, 'severity': 'high'},
            'jerking': {'weight': 9, 'severity': 'high'},
            'stiffness': {'weight': 8, 'severity': 'high'},
            'twitching': {'weight': 8, 'severity': 'high'},
            
            # Medium severity symptoms
            'confusion': {'weight': 7, 'severity': 'medium'},
            'dizziness': {'weight': 6, 'severity': 'medium'},
            'disorientation': {'weight': 7, 'severity': 'medium'},
            'memory loss': {'weight': 6, 'severity': 'medium'},
            'blank stare': {'weight': 6, 'severity': 'medium'},
            'unresponsive': {'weight': 7, 'severity': 'medium'},
            'tremor': {'weight': 6, 'severity': 'medium'},
            'shaking': {'weight': 6, 'severity': 'medium'},
            
            # Low-medium severity symptoms
            'headache': {'weight': 4, 'severity': 'low-medium'},
            'nausea': {'weight': 4, 'severity': 'low-medium'},
            'fatigue': {'weight': 3, 'severity': 'low-medium'},
            'weakness': {'weight': 4, 'severity': 'low-medium'},
            'numbness': {'weight': 5, 'severity': 'low-medium'},
            'tingling': {'weight': 4, 'severity': 'low-medium'},
            
            # Aura symptoms (pre-seizure)
            'aura': {'weight': 7, 'severity': 'medium'},
            'strange smell': {'weight': 6, 'severity': 'medium'},
            'strange taste': {'weight': 6, 'severity': 'medium'},
            'visual disturbance': {'weight': 6, 'severity': 'medium'},
            'déjà vu': {'weight': 5, 'severity': 'medium'},
            'anxiety': {'weight': 4, 'severity': 'low-medium'},
            'fear': {'weight': 5, 'severity': 'medium'},
        }
        
        # Condition patterns
        self.conditions = {
            'SEIZURE': {
                'keywords': ['seizure', 'convulsion', 'unconscious', 'jerking', 'collapse'],
                'description': 'Active seizure symptoms detected'
            },
            'PREICTAL': {
                'keywords': ['aura', 'confusion', 'dizziness', 'strange smell', 'strange taste', 'anxiety'],
                'description': 'Pre-seizure warning signs detected'
            },
            'POST-ICTAL': {
                'keywords': ['confusion', 'fatigue', 'memory loss', 'weakness', 'headache'],
                'description': 'Post-seizure recovery symptoms'
            },
            'NORMAL': {
                'keywords': [],
                'description': 'No significant seizure-related symptoms'
            }
        }
    
    def analyze_symptoms(self, symptom_text: str) -> Dict:
        """Main method to analyze symptom text"""
        # Normalize text
        text = symptom_text.lower().strip()
        
        # Find matching symptoms
        detected_symptoms = self.detect_symptoms(text)
        
        # Calculate risk score
        risk_score = self.calculate_risk_score(detected_symptoms)
        
        # Determine risk level
        risk_level = self.determine_risk_level(risk_score)
        
        # Identify possible condition
        condition = self.identify_condition(detected_symptoms)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(risk_level, condition, detected_symptoms)
        
        # Create result
        result = {
            'detected_symptoms': detected_symptoms,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'possible_condition': condition,
            'recommendations': recommendations,
            'urgency': self.get_urgency_level(risk_level),
            'explanation': self.generate_explanation(detected_symptoms, risk_level, condition)
        }
        
        return result
    
    def detect_symptoms(self, text: str) -> List[Dict]:
        """Detect symptoms from text"""
        detected = []
        
        for symptom, info in self.symptom_keywords.items():
            if symptom in text:
                detected.append({
                    'symptom': symptom,
                    'weight': info['weight'],
                    'severity': info['severity']
                })
        
        return detected
    
    def calculate_risk_score(self, detected_symptoms: List[Dict]) -> float:
        """Calculate overall risk score (0-100)"""
        if not detected_symptoms:
            return 0.0
        
        total_weight = sum(s['weight'] for s in detected_symptoms)
        max_possible = 10 * len(detected_symptoms)  # Max weight is 10
        
        # Normalize to 0-100 scale
        risk_score = min((total_weight / max_possible) * 100, 100)
        
        return round(risk_score, 2)
    
    def determine_risk_level(self, risk_score: float) -> str:
        """Determine risk level from score"""
        if risk_score >= 70:
            return 'HIGH'
        elif risk_score >= 40:
            return 'MEDIUM'
        elif risk_score >= 20:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def identify_condition(self, detected_symptoms: List[Dict]) -> str:
        """Identify most likely condition"""
        if not detected_symptoms:
            return 'NORMAL'
        
        symptom_names = [s['symptom'] for s in detected_symptoms]
        
        # Check each condition
        condition_scores = {}
        for condition, info in self.conditions.items():
            matches = sum(1 for kw in info['keywords'] if kw in symptom_names)
            condition_scores[condition] = matches
        
        # Get condition with highest matches
        best_condition = max(condition_scores.items(), key=lambda x: x[1])
        
        if best_condition[1] > 0:
            return best_condition[0]
        else:
            # Check severity
            high_severity = any(s['severity'] == 'high' for s in detected_symptoms)
            if high_severity:
                return 'SEIZURE'
            else:
                return 'PREICTAL'
    
    def generate_recommendations(self, risk_level: str, condition: str, symptoms: List[Dict]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        if risk_level == 'HIGH':
            recommendations.extend([
                "⚠️ URGENT: Seek immediate medical attention",
                "Call emergency services (911) if experiencing active seizure",
                "Do not leave the person alone",
                "Ensure safety - remove nearby hazards",
                "Time the seizure duration"
            ])
        elif risk_level == 'MEDIUM':
            recommendations.extend([
                "Consult a neurologist as soon as possible",
                "Monitor symptoms closely",
                "Avoid driving or operating machinery",
                "Stay in a safe environment",
                "Keep a symptom diary"
            ])
        elif risk_level == 'LOW':
            recommendations.extend([
                "Schedule an appointment with a neurologist",
                "Track your symptoms",
                "Maintain regular sleep schedule",
                "Avoid known triggers (stress, lack of sleep, alcohol)",
                "Consider keeping a seizure diary"
            ])
        else:
            recommendations.extend([
                "Continue monitoring your health",
                "Maintain healthy lifestyle habits",
                "Consult a doctor if symptoms worsen"
            ])
        
        # Add condition-specific recommendations
        if condition == 'PREICTAL':
            recommendations.append("You may be experiencing pre-seizure warning signs - take precautions")
        
        return recommendations
    
    def get_urgency_level(self, risk_level: str) -> str:
        """Get urgency level"""
        urgency_map = {
            'HIGH': 'IMMEDIATE',
            'MEDIUM': 'URGENT',
            'LOW': 'ROUTINE',
            'MINIMAL': 'NON-URGENT'
        }
        return urgency_map.get(risk_level, 'ROUTINE')
    
    def generate_explanation(self, symptoms: List[Dict], risk_level: str, condition: str) -> str:
        """Generate detailed explanation"""
        if not symptoms:
            return "No significant seizure-related symptoms detected. Continue monitoring your health."
        
        symptom_list = ', '.join([s['symptom'] for s in symptoms])
        
        explanation = f"Based on your symptoms ({symptom_list}), "
        
        if risk_level == 'HIGH':
            explanation += f"you are showing signs of {condition.lower()} which requires immediate medical attention. "
        elif risk_level == 'MEDIUM':
            explanation += f"you may be experiencing {condition.lower()} symptoms. Medical consultation is recommended. "
        else:
            explanation += f"you have mild symptoms that should be monitored. "
        
        explanation += f"Risk level: {risk_level}. Please follow the recommendations provided."
        
        return explanation


if __name__ == "__main__":
    # Test symptom checker
    checker = SymptomChecker()
    
    # Test cases
    test_symptoms = [
        "I feel dizziness and confusion",
        "I had a seizure with jerking movements",
        "I'm experiencing aura and strange smells",
        "Just feeling a bit tired"
    ]
    
    for symptom in test_symptoms:
        print(f"\n{'='*60}")
        print(f"Symptom: {symptom}")
        result = checker.analyze_symptoms(symptom)
        print(f"Risk Level: {result['risk_level']}")
        print(f"Condition: {result['possible_condition']}")
        print(f"Urgency: {result['urgency']}")
        print(f"Explanation: {result['explanation']}")
