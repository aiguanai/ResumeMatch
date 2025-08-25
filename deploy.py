#!/usr/bin/env python3
"""
Deployment script for Resume Matching API
This script helps set up the environment and start the server.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def check_virtual_environment():
    """Check if virtual environment is activated"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment is activated")
        return True
    else:
        print("⚠ Virtual environment is not activated")
        print("  Consider creating and activating a virtual environment:")
        print("  python -m venv venv")
        print("  # On Windows: venv\\Scripts\\activate")
        print("  # On macOS/Linux: source venv/bin/activate")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask', 'openai', 'python-dotenv', 'textract', 
        'PyPDF2', 'python-docx', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is missing")
    
    if missing_packages:
        print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✓ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("✗ Failed to install dependencies")
            return False
    
    return True

def check_environment_file():
    """Check if .env file exists and has required variables"""
    env_file = Path('.env')
    env_example = Path('env_example.txt')
    
    if not env_file.exists():
        if env_example.exists():
            print("Creating .env file from template...")
            shutil.copy(env_example, env_file)
            print("✓ .env file created")
            print("⚠ Please edit .env file and add your OpenAI API key")
            return False
        else:
            print("✗ No .env file found and no template available")
            return False
    
    # Check if OPENAI_API_KEY is set
    with open(env_file, 'r') as f:
        content = f.read()
        if 'OPENAI_API_KEY=your_openai_api_key_here' in content or 'OPENAI_API_KEY=' not in content:
            print("⚠ Please set your OpenAI API key in the .env file")
            return False
    
    print("✓ .env file is properly configured")
    return True

def check_resumes_directory():
    """Check if resumes directory exists and has files"""
    resumes_dir = Path('resumes')
    if not resumes_dir.exists():
        print("Creating resumes directory...")
        resumes_dir.mkdir()
        print("✓ Resumes directory created")
        print("⚠ Please add resume files to the resumes/ directory")
        return False
    
    resume_files = list(resumes_dir.glob('*.pdf')) + list(resumes_dir.glob('*.docx')) + list(resumes_dir.glob('*.doc')) + list(resumes_dir.glob('*.txt'))
    if not resume_files:
        print("⚠ No resume files found in resumes/ directory")
        print("  Supported formats: PDF, DOCX, DOC, TXT")
        return False
    
    print(f"✓ Found {len(resume_files)} resume files")
    return True

def start_server():
    """Start the Flask server"""
    print("\nStarting Resume Matching API server...")
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")

def main():
    """Main deployment function"""
    print("Resume Matching API - Deployment Script")
    print("=" * 50)
    
    # Run all checks
    checks = [
        check_python_version,
        check_virtual_environment,
        check_dependencies,
        check_environment_file,
        check_resumes_directory
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
        print()
    
    if not all_passed:
        print("Some checks failed. Please fix the issues above before starting the server.")
        print("\nQuick setup guide:")
        print("1. Create virtual environment: python -m venv venv")
        print("2. Activate virtual environment:")
        print("   - Windows: venv\\Scripts\\activate")
        print("   - macOS/Linux: source venv/bin/activate")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Set OpenAI API key in .env file")
        print("5. Add resume files to resumes/ directory")
        print("6. Run this script again")
        return
    
    print("✓ All checks passed!")
    
    # Ask user if they want to start the server
    response = input("\nDo you want to start the server now? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        start_server()
    else:
        print("To start the server manually, run: python app.py")

if __name__ == "__main__":
    main()
