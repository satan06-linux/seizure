#!/bin/bash
# Script to push SeizureGuard AI to GitHub

echo "🚀 SeizureGuard AI - GitHub Push Script"
echo "========================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

echo "📝 Step 1: Initialize Git repository"
git init

echo ""
echo "📝 Step 2: Add all files"
git add .

echo ""
echo "📝 Step 3: Create initial commit"
git commit -m "Initial commit: SeizureGuard AI v1.0.0

- Complete AI-powered seizure detection system
- Multi-format file processing (CSV, PDF, Image, EDF)
- Intelligent symptom checker
- AI chatbot assistant
- Neurologist finder
- Beautiful Streamlit interface
- Comprehensive documentation
- Production-ready code"

echo ""
echo "📝 Step 4: Rename branch to main"
git branch -M main

echo ""
echo "⚠️  IMPORTANT: Create GitHub repository first!"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: seizureguard-ai"
echo "3. Description: AI-powered seizure detection and neurologist recommendation system"
echo "4. Choose Public or Private"
echo "5. DO NOT initialize with README, .gitignore, or license"
echo "6. Click 'Create repository'"
echo ""
read -p "Press Enter after creating the GitHub repository..."

echo ""
read -p "Enter your GitHub username: " username
read -p "Enter repository name (default: seizureguard-ai): " reponame
reponame=${reponame:-seizureguard-ai}

echo ""
echo "📝 Step 5: Add remote origin"
git remote add origin "https://github.com/$username/$reponame.git"

echo ""
echo "📝 Step 6: Push to GitHub"
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🎉 Your repository is now live at:"
echo "   https://github.com/$username/$reponame"
echo ""
echo "📋 Next steps:"
echo "1. Add topics: machine-learning, healthcare, seizure-detection, epilepsy, streamlit"
echo "2. Add description in repository settings"
echo "3. Deploy to Streamlit Cloud: https://share.streamlit.io"
echo "4. Create first release (v1.0.0)"
echo "5. Share with the community!"
echo ""
echo "📖 See GITHUB_SETUP.md for detailed instructions"
