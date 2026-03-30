@echo off
echo 플라스크 서버를 시작합니다... 브라우저가 열릴 때까지 잠시 기다려주세요.
start http://127.0.0.1:5000/
python app.py
pause
