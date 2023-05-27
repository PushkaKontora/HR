dev:
	python src/manage.py runserver

pshell:
	PIPENV_DONT_LOAD_ENV=1 pipenv shell

run:
	cd src && gunicorn config.wsgi:application -w 2 --bind :8000

lint:
	isort . & \
	flake8 --config setup.cfg & \
	black --config pyproject.toml .

check:
	isort --check --diff .
	flake8 --config setup.cfg
	black --check --config pyproject.toml .

migration:
	python src/manage.py makemigrations -n ${n}

migrate:
	python src/manage.py migrate ${o}

# Tests

test:
	cd src && pytest --disable-warnings

unit:
	cd src && pytest -m unit --disable-warnings

smoke:
	cd src && pytest -m smoke --disable-warnings

integration:
	cd src && pytest -m integration --disable-warnings


# Only dev management commands

initvacancies:
	python src/manage.py initvacancies
