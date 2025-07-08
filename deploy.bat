@echo off
echo 🚀 Preparing AI Content Extractor for Streamlit Cloud deployment...

:: Check if git is initialized
if not exist ".git" (
    echo ❌ Git repository not found. Initializing...
    git init
    git remote add origin https://github.com/yourusername/ai-content-extractor.git
)

:: Check for required files
echo ✅ Checking required files...
set "missing_files="

if exist "main.py" (echo   ✓ main.py) else (echo   ❌ main.py ^(missing^) && set "missing_files=1")
if exist "scrape_deploy.py" (echo   ✓ scrape_deploy.py) else (echo   ❌ scrape_deploy.py ^(missing^) && set "missing_files=1")
if exist "parse_deploy.py" (echo   ✓ parse_deploy.py) else (echo   ❌ parse_deploy.py ^(missing^) && set "missing_files=1")
if exist "data_processor.py" (echo   ✓ data_processor.py) else (echo   ❌ data_processor.py ^(missing^) && set "missing_files=1")
if exist "requirements.txt" (echo   ✓ requirements.txt) else (echo   ❌ requirements.txt ^(missing^) && set "missing_files=1")
if exist ".streamlit\config.toml" (echo   ✓ .streamlit/config.toml) else (echo   ❌ .streamlit/config.toml ^(missing^) && set "missing_files=1")
if exist ".gitignore" (echo   ✓ .gitignore) else (echo   ❌ .gitignore ^(missing^) && set "missing_files=1")

if defined missing_files (
    echo Some required files are missing. Please ensure all files are present.
    pause
    exit /b 1
)

:: Check requirements.txt
echo ✅ Validating requirements.txt...
findstr /i "streamlit" requirements.txt >nul
if %errorlevel% == 0 (
    echo   ✓ Streamlit found
) else (
    echo   ❌ Streamlit not found in requirements.txt
    pause
    exit /b 1
)

:: Add and commit files
echo 📦 Adding files to git...
git add .
git status

echo 💾 Committing changes...
git commit -m "Prepare for Streamlit Cloud deployment"

echo 🔄 Pushing to GitHub...
git push -u origin main

echo.
echo 🎉 Deployment preparation complete!
echo.
echo Next steps:
echo 1. Visit https://share.streamlit.io
echo 2. Connect your GitHub account
echo 3. Select your repository
echo 4. Set main file as 'main.py'
echo 5. Click Deploy!
echo.
echo Your app will be available at: https://your-app-name.streamlit.app
pause
