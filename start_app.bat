echo off
set FLASK_APP=netbank
set FLASK_ENV=development
start "Chrome" chrome http://127.0.0.1:5000
pip install -e
flask run