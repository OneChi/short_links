WORKDIR=../bin

echo '1. Collection static files ...'
poetry run ./manage.py collectstatic --noinput

echo '2. Migrate...'
poetry run ./manage.py migrate

echo "3. Load fixtures..."
bash $WORKDIR/load-data.prod.sh

echo '4. Start Django...'
poetry run ./manage.py runserver 0.0.0.0:8000
