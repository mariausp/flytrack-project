# FlyTrack

## Como rodar
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py runserver

Acesse http://127.0.0.1:8000/
