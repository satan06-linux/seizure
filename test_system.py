"""
System Test Script
Tests all modules to ensure they work correctly
"""
import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    try:
        from modules.trainer import SeizureModelTrainer
        from modules.predictor import SeizurePredictor
        from modules.file_processor import FileProcessor
        from modules.symptom_checker import SymptomChecker
        from modules.chatbot import SeizureChatbot
        from modules.doctor_recommender import DoctorRecommender
        print("✓ All modules imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import error: {str(e)}")
        return False


def test_symptom_checker():
    """Test symptom checker module"""
    print("\nTesting Symptom Checker...")
    try:
        from modules.symptom_checker import SymptomChecker
        
        checker = SymptomChecker()
        result = checker.analyze_symptoms("I feel dizziness and confusion")
        
        assert 'risk_level' in result
        assert 'detected_symptoms' in result
        assert 'recommendations' in result
        
        print(f"✓ Symptom Checker working")
        print(f"  - Risk Level: {result['risk_level']}")
        print(f"  - Detected: {len(result['detected_symptoms'])} symptoms")
        return True
    except Exception as e:
        print(f"✗ Symptom Checker error: {str(e)}")
        return False


def test_chatbot():
    """Test chatbot module"""
    print("\nTesting Chatbot...")
    try:
        from modules.chatbot import SeizureChatbot
        
        bot = SeizureChatbot()
        response = bot.chat("What is a seizure?")
        
        assert 'message' in response
        assert len(response['message']) > 0
        
        print(f"✓ Chatbot working")
        print(f"  - Response length: {len(response['message'])} chars")
        return True
    except Exception as e:
        print(f"✗ Chatbot error: {str(e)}")
        return False


def test_doctor_recommender():
    """Test doctor recommender module"""
    print("\nTesting Doctor Recommender...")
    try:
        from modules.doctor_recommender import DoctorRecommender
        
        recommender = DoctorRecommender()
        doctors = recommender.recommend_doctors(top_n=3)
        
        assert len(doctors) > 0
        assert 'name' in doctors[0]
        assert 'phone' in doctors[0]
        
        print(f"✓ Doctor Recommender working")
        print(f"  - Found {len(doctors)} doctors")
        return True
    except Exception as e:
        print(f"✗ Doctor Recommender error: {str(e)}")
        return False


def test_file_processor():
    """Test file processor module"""
    print("\nTesting File Processor...")
    try:
        from modules.file_processor import FileProcessor
        
        processor = FileProcessor()
        
        # Test supported formats
        assert 'csv' in processor.supported_formats
        assert 'pdf' in processor.supported_formats
        
        print(f"✓ File Processor initialized")
        print(f"  - Supported formats: {', '.join(processor.supported_formats)}")
        return True
    except Exception as e:
        print(f"✗ File Processor error: {str(e)}")
        return False


def test_predictor():
    """Test predictor module (requires trained model)"""
    print("\nTesting Predictor...")
    try:
        from modules.predictor import SeizurePredictor
        import numpy as np
        
        predictor = SeizurePredictor()
        
        # Create dummy features
        dummy_features = {col: np.random.randn() for col in predictor.feature_columns}
        
        result = predictor.predict(dummy_features)
        
        assert 'prediction' in result
        assert 'confidence' in result
        assert 'risk_level' in result
        
        print(f"✓ Predictor working")
        print(f"  - Prediction: {result['prediction']}")
        print(f"  - Confidence: {result['confidence']:.2f}%")
        return True
    except FileNotFoundError:
        print(f"⚠ Predictor: Model not found (train model first)")
        return None  # Not a failure, just not trained yet
    except Exception as e:
        print(f"✗ Predictor error: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("SeizureGuard AI - System Test")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Symptom Checker", test_symptom_checker()))
    results.append(("Chatbot", test_chatbot()))
    results.append(("Doctor Recommender", test_doctor_recommender()))
    results.append(("File Processor", test_file_processor()))
    results.append(("Predictor", test_predictor()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    skipped = sum(1 for _, result in results if result is None)
    
    for name, result in results:
        if result is True:
            status = "✓ PASS"
        elif result is False:
            status = "✗ FAIL"
        else:
            status = "⚠ SKIP"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed == 0:
        print("\n🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        if skipped > 0:
            print("1. Generate dataset: python generate_sample_dataset.py")
            print("2. Train model: python modules/trainer.py")
        print("3. Run app: streamlit run app.py")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
    
    print("="*60)


if __name__ == "__main__":
    main()
