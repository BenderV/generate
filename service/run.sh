echo $DATABASE_URL
python model.py
gunicorn -b 0.0.0.0:5000 app:app
