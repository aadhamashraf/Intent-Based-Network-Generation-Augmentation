#!/usr/bin/env python3
"""
Environment setup script for Intent-Based Network Generation Augmentation toolkit.
"""
import os
import sys
import subprocess
import importlib.util


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def install_requirements():
    """Install required packages."""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False
    return True


def download_models():
    """Download required models."""
    print("Downloading required models...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_md"])
        print("✓ spaCy model downloaded")
    except subprocess.CalledProcessError:
        print("⚠ Failed to download spaCy model. Some features may not work.")
    
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        print("✓ NLTK data downloaded")
    except Exception as e:
        print(f"⚠ Failed to download NLTK data: {e}")


def check_optional_dependencies():
    """Check optional dependencies."""
    print("Checking optional dependencies...")
    
    optional_deps = {
        'torch': 'PyTorch (for GPU acceleration)',
        'transformers': 'Transformers (for advanced NLP)',
        'sentence_transformers': 'Sentence Transformers (for semantic analysis)',
        'spacy': 'spaCy (for NLP processing)'
    }
    
    for dep, description in optional_deps.items():
        if importlib.util.find_spec(dep) is not None:
            print(f"✓ {description}")
        else:
            print(f"⚠ {description} - not installed")


def create_directories():
    """Create necessary directories."""
    directories = [
        'data',
        'output',
        'logs',
        'models',
        'cache'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")


def test_installation():
    """Test the installation."""
    print("Testing installation...")
    
    try:
        sys.path.insert(0, 'src')
        from Intents_Generators.Advanced3GPPIntentGenerator import Advanced3GPPIntentGenerator
        from config import parse_args
        
        generator = Advanced3GPPIntentGenerator(use_llm_synthesis=False)
        print("✓ Generator creation successful")
        
        intent = generator.generate_intent()
        print("✓ Intent generation successful")
        
        print("✓ Installation test passed")
        return True
        
    except Exception as e:
        print(f"✗ Installation test failed: {e}")
        return False


def main():
    """Main setup function."""
    print("Setting up Intent-Based Network Generation Augmentation toolkit...")
    print("=" * 60)
    
    check_python_version()
    
    if not install_requirements():
        print("Setup failed. Please check the error messages above.")
        sys.exit(1)
    
    download_models()
    
    check_optional_dependencies()
    
    create_directories()
    
    if test_installation():
        print("\n" + "=" * 60)
        print("✓ Setup completed successfully!")
        print("\nYou can now run:")
        print("  python src/main.py --num_records 10")
        print("  make generate")
        print("  python -m pytest tests/")
    else:
        print("\n" + "=" * 60)
        print("⚠ Setup completed with warnings.")
        print("Some features may not work properly.")
        print("Please check the error messages above.")


if __name__ == "__main__":
    main()