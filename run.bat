
python -m venv env_name
call env_name\Scripts\activate
pip install -r requirements.txt
pip freeze > requirements.txt
cd src
python main.py
@echo off
pause