#!/bin/sh
python replacer.py
flask db upgrade
exec gunicorn -b 0.0.0.0:8000 --reload --access-logfile - main:app
