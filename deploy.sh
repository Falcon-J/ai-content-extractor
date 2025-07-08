#!/bin/bash

# Deployment preparation script for AI Content Extractor

echo "🚀 Preparing AI Content Extractor for Streamlit Cloud deployment..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Initializing..."
    git init
    git remote add origin https://github.com/yourusername/ai-content-extractor.git
fi

# Check for required files
required_files=(
    "main.py"
    "scrape_deploy.py"
    "parse_deploy.py"
    "data_processor.py"
    "requirements.txt"
    ".streamlit/config.toml"
    ".gitignore"
)

echo "✅ Checking required files..."
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ❌ $file (missing)"
        exit 1
    fi
done

# Check requirements.txt
echo "✅ Validating requirements.txt..."
if grep -q "streamlit" requirements.txt; then
    echo "  ✓ Streamlit found"
else
    echo "  ❌ Streamlit not found in requirements.txt"
    exit 1
fi

# Add and commit files
echo "📦 Adding files to git..."
git add .
git status

echo "💾 Committing changes..."
git commit -m "Prepare for Streamlit Cloud deployment"

echo "🔄 Pushing to GitHub..."
git push -u origin main

echo ""
echo "🎉 Deployment preparation complete!"
echo ""
echo "Next steps:"
echo "1. Visit https://share.streamlit.io"
echo "2. Connect your GitHub account"
echo "3. Select your repository"
echo "4. Set main file as 'main.py'"
echo "5. Click Deploy!"
echo ""
echo "Your app will be available at: https://your-app-name.streamlit.app"
