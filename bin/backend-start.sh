WORKDIR=../bin

echo '1. Collection static files ...'
poetry run ./manage.py collectstatic --noinput

echo '2. Migrate...'
poetry run ./manage.py migrate

echo '3. Create superuser for debugging...'
bash $WORKDIR/create_superuser.sh

echo "4. Load fixtures..."
bash $WORKDIR/load-data.sh

echo '5. Start Django...'
poetry run ./manage.py runserver 0.0.0.0:8000
