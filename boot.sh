#!/bin/bash
source venv/bin/activate
flask db upgrade
exec gunicorn -b :8090 --access-logfile - --error-logfile - app_entry:app