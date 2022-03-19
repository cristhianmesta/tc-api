# TC-API: API DE TIPO DE CAMBIO

## Crear un entorno virtual

- $ py -m venv venv
- $ . venv/scripts/activate

## Paquetes

- $ pip install Flask
- $ pip install pyodbc‑4.0.32‑cp310‑cp310‑win_amd64.whl (https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyodbc)

## Ejecutar

- $ export FLASK_APP=app.py
- $ export FLASK_ENV=development (Sólo para desarrollo)
- $ flask run