#! /bin/sh
uwsgi --http 0.0.0.0:5000 --module quickclip:app --master --processes 3 --threads 3 --log-x-forwarded-for