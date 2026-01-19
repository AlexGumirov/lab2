# Django DB Dashboard (PostgreSQL + Jinja2)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python manage.py import_leagues_csv --path top_expensive_leagues.csv
python manage.py runserver
```