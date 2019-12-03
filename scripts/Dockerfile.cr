FROM api-container
CMD uwsgi --http :${CC_PORT} --wsgi-file uwsgi.py --master --processes 4 --threads 2 --stats :9191
EXPOSE 9000:9000
