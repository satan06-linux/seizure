"""
QuickStart Script for SeizureGuard AI
Automates the complete setup process
"""
import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print("✓ Python version is compatible")
    return True


def install_dependencies():
    """Install required packages"""
    print_header("Installing Dependencies")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"])
        print("✓ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = ['models', 'datasets', 'temp']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created/verified: {directory}/")
    
    return True


def generate_dataset():
    """Generate sample dataset"""
    print_header("Generating Sample Dataset")
    
    dataset_path = 'datasets/seizure_dataset.csv'
    
    if os.path.exists(dataset_path):
        response = input(f"\nDataset already exists at {dataset_path}. Regenerate? (y/n): ")
        if response.lower() != 'y':
            print("✓ Using existing dataset")
            return True
    
    try:
        print("Generating synthetic dataset...")
        from generate_sample_dataset import generate_sample_dataset
        generate_sample_dataset(n_samples=1000, n_features=20)
        print("✓ Sample dataset generated successfully")
        return True
    except Exception as e:
        print(f"❌ Error generating dataset: {e}")
        return False


def train_model():
    """Train the machine learning model"""
    print_header("Training Model")
    
    model_path = 'models/seizure_model.pkl'
    
    if os.path.exists(model_path):
        response = input(f"\nModel already exists at {model_path}. Retrain? (y/n): ")
        if response.lower() != 'y':
            print("✓ Using existing model")
            return True
    
    try:
        print("Training RandomForest model...")
        print("This may take a few minutes...\n")
        
        from modules.trainer import SeizureModelTrainer
        trainer = SeizureModelTrainer()
        accuracy = trainer.run_training_pipeline()
        
        print(f"\n✓ Model trained successfully with {accuracy*100:.2f}% accuracy")
        return True
    except Exception as e:
        print(f"❌ Error training model: {e}")
        return False


def run_tests():
    """Run system tests"""
    print_header("Running System Tests")
    
    try:
        print("Testing all modules...\n")
        
        # Import test script
        from test_system import (
            test_imports,
            test_symptom_checker,
            test_chatbot,
            test_doctor_recommender,
            test_file_processor,
            test_predictor
        )
        
        results = []
        results.append(("Imports", test_imports()))
        results.append(("Symptom Checker", test_symptom_checker()))
        results.append(("Chatbot", test_chatbot()))
        results.append(("Doctor Recommender", test_doctor_recommender()))
        results.append(("File Processor", test_file_processor()))
        results.append(("Predictor", test_predictor()))
        
        # Count results
        passed = sum(1 for _, result in results if result is True)
        failed = sum(1 for _, result in results if result is False)
        
        print(f"\n✓ Tests completed: {passed} passed, {failed} failed")
        
        return failed == 0
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def launch_app():
    """Launch Streamlit application"""
    print_header("Launching Application")
    
    print("\nStarting Streamlit server...")
    print("The application will open in your default browser.")
    print("\nPress Ctrl+C to stop the server.\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\nApplication stopped.")
    except Exception as e:
        print(f"❌ Error launching app: {e}")
        print("\nTry running manually: streamlit run app.py")


def main():
    """Main quickstart function"""
    print("\n" + "🧠"*30)
    print("  SeizureGuard AI - QuickStart Setup")
    print("🧠"*30)
    
    # Step 1: Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Incompatible Python version")
        return
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        return
    
    # Step 3: Create directories
    if not create_directories():
        print("\n❌ Setup failed: Could not create directories")
        return
    
    # Step 4: Generate dataset
    if not generate_dataset():
        print("\n❌ Setup failed: Could not generate dataset")
        return
    
    # Step 5: Train model
    if not train_model():
        print("\n❌ Setup failed: Could not train model")
        return
    
    # Step 6: Run tests
    print("\nWould you like to run system tests? (recommended)")
    response = input("Run tests? (y/n): ")
    if response.lower() == 'y':
        run_tests()
    
    # Step 7: Launch app
    print_header("Setup Complete!")
    
    print("\n✅ SeizureGuard AI is ready to use!")
    print("\nSetup Summary:")
    print("  ✓ Dependencies installed")
    print("  ✓ Directories created")
    print("  ✓ Dataset generated")
    print("  ✓ Model trained")
    print("  ✓ System tested")
    
    print("\n" + "="*60)
    print("Next Steps:")
    print("="*60)
    print("\n1. Launch the application:")
    print("   streamlit run app.py")
    print("\n2. Open your browser to:")
    print("   http://localhost:8501")
    print("\n3. Explore the features:")
    print("   • Upload EEG files")
    print("   • Check symptoms")
    print("   • Chat with AI assistant")
    print("   • Find neurologists")
    
    print("\n" + "="*60)
    
    # Ask to launch
    response = input("\nWould you like to launch the app now? (y/n): ")
    if response.lower() == 'y':
        launch_app()
    else:
        print("\nYou can launch the app later with: streamlit run app.py")
    
    print("\n🎉 Thank you for using SeizureGuard AI!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("\nPlease check the error and try again.")
