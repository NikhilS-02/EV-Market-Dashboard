@echo off
echo ===== EV Market Analytics - Flask website =====
pip install flask python-dotenv
echo.
set /p DASH=Paste your Tableau DASHBOARD link and press Enter: 
set /p STORY=Paste your Tableau STORY link and press Enter: 
(
echo TABLEAU_DASHBOARD_URL=%DASH%
echo TABLEAU_STORY_URL=%STORY%
) > .env
echo.
echo Opening http://127.0.0.1:5000 ... keep this window open while you record.
start http://127.0.0.1:5000
python app.py
pause
