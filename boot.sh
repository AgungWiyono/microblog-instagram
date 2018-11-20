#!/bin/sh
flask db uprade
exec gunicorn -b 0.0.0.0:8000 --reload --access-logfile - main:app
