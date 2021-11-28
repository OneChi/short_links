# run django without container
# do 
#'''bash
# 	export $(cat ../env/backend.env)
#'''
run_local:
	docker-compose -f docker-compose.db.yml up -d
	poetry run ./manage.py runserver localhost:8000

migrations:
	poetry run ./manage.py makemigrations

migrate:
	poetry run ./manage.py migrate

sync_db:
	poetry run ./manage.py makemigrations
	poetry run ./manage.py migrate

reset:
	# Reset all containers create in project.
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down --volumes --remove-orphans

# Testing.
test_start: reset
	# Run database for tests.
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

test_run:
	# Run pytest.
	docker exec sl.backend pytest

test_end:
	# Run tests.
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down --volumes

test: test_start test_run reset test_end
	# Run tests.
	echo Test finished!

build:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build


codestyle:
	poetry run autopep8 . -r --in-place
	poetry run isort .

mypy:
	poetry run mypy --config-file=setup.cfg .

flake8:
	poetry run flake8 .