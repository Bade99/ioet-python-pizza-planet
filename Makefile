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

## update-db |-| update the database with the new fields
update-db:
	python manage.py db migrate
	python manage.py db upgrade

## reset-db |-| delete the database and regenerate it
reset-db:
	del pizza.sqlite
	python manage.py db upgrade

## populate-db |-| populate the database with test data
populate-db:
	python manage.py populate

## start |-| start the app
start:
	python manage.py run

## tests |-| run tests
test:
	python -m pytest -v app/test

## test-coverage |-| run test-coverage
test-coverage:
	python -m pytest -v --cov-report=term-missing --cov=app app/test

## ci-test-coverage |-| same as test-coverage, but only to be used in github actions
ci-test-coverage:
	python -m pytest -v --cov-report=term-missing --cov=app app/test > pytest-coverage.txt

## lint |-| run linter
lint:
	flake8 app/

## format |-| run formatter
format:
	autopep8 --max-line-length 100 --experimental -i -r app/
