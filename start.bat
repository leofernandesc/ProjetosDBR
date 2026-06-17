@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Criando ambiente virtual...
    python -m venv .venv
)
call .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py --server.port 8501
pause