#!/bin/sh
PYTHONPATH=. gunicorn web.app:server --workers 1 --timeout 180 --bind 0.0.0.0:8080
