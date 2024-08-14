## create-venv |-| create virtual environment
create-venv:
	python -m venv .venv

## activate-venv |-| activate virtual environment
activate-venv:
	. .venv/Scripts/activate

## install-dependencies |-| install development dependencies
install-dependencies:
	pip install -r requirements.txt

## start-db |-| start the database
start-db:
	python manage.py db init
	python manage.py db migrate
	python manage.py db upgrade

reset-db:
	del pizza.sqlite
	python manage.py db upgrade

## start |-| start the app
start:
	python manage.py run

## run-tests |-| run tests
test:
	python manage.py test
