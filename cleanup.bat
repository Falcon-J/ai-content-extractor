@echo off
echo 🧹 Cleaning up unnecessary files...

REM Remove all the extra files we don't need
del /q CLEANUP_GUIDE.md 2>nul
del /q deploy.bat 2>nul
del /q deploy.sh 2>nul
del /q DEPLOYMENT.md 2>nul
del /q DEPLOYMENT_FIXES.md 2>nul
del /q docker-compose.yml 2>nul
del /q Dockerfile 2>nul
del /q DOCKER_ALTERNATIVES.md 2>nul
del /q EXTRACTION_FIXES.md 2>nul
del /q main.py 2>nul
del /q OLLAMA_DEPLOYMENT.md 2>nul
del /q parse.py 2>nul
del /q parse_ai_deploy.py 2>nul
del /q parse_cloud_ai.py 2>nul
del /q parse_deploy.py 2>nul
del /q requirements-cloud-ai.txt 2>nul
del /q requirements-deploy.txt 2>nul
del /q scrape_deploy.py 2>nul
del /q setup-groq.bat 2>nul
del /q setup-groq.sh 2>nul
del /q setup-native-ollama.bat 2>nul
del /q setup-native-ollama.sh 2>nul
del /q setup-no-docker.bat 2>nul
del /q setup-no-docker.sh 2>nul
del /q start-ai.bat 2>nul
del /q start-ai.sh 2>nul
del /q STREAMLIT_DEPLOYMENT.md 2>nul
del /q test_deployment.py 2>nul
del /q test_setup.py 2>nul
del /q data_processor.py 2>nul

REM Remove .streamlit folder
rmdir /s /q .streamlit 2>nul

REM Remove __pycache__ folder
rmdir /s /q __pycache__ 2>nul

echo ✅ Cleanup complete!
echo 📁 Remaining files:
echo   - simple_app.py (main app)
echo   - requirements.txt (dependencies)
echo   - .env (API configuration)
echo   - scrape.py (scraping logic)
echo   - run_app.bat (launcher)
echo   - QUICK_START.md (usage guide)
echo   - README.md (documentation)
echo   - status_check.py (status checker)
echo   - test_app.py (testing)
echo.
echo 🚀 Your streamlined AI web scraper is ready!
echo 💡 Run: run_app.bat
pause
