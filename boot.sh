#!/bin/sh
exec gunicorn -b :80 flask_app:application
