# Django DB Dashboard (PostgreSQL + Jinja2)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d
python manage.py migrate --noinput
python manage.py import_leagues_csv --path top_expensive_leagues.csv
python manage.py runserver 0.0.0.0:8000
```