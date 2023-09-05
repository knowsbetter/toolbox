# Minimal toolbox for B748.
This project helps to search part numbers listed in AIPC of B738F aircraft.

# Instructions
To start the server:<br>
1. $ pip install -r requirements.txt
2. $ uvicorn server.main:app --host 0.0.0.0 --port 8000
3. FastAPI backend version is available at route "/".
4. JavaScript version is available at route "/js". For tests only. Will be deleted soon :)
