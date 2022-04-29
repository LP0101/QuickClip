#! /bin/sh
uwsgi --http 0.0.0.0:5000 --module quickclip:app --master --processes 4 --threads 4 --log-x-forwarded-for