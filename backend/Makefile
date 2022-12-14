dev:
	pipenv run python src/manage.py runserver

run:
	cd src && pipenv run gunicorn -c config/gunicorn.conf.py config.wsgi:application

lint:
	pipenv run isort . & \
	pipenv run flake8 --config setup.cfg & \
	pipenv run black --config pyproject.toml .

check:
	pipenv run isort --check --diff .
	pipenv run flake8 --config setup.cfg
	pipenv run black --check --config pyproject.toml .

migration:
	pipenv run python src/manage.py makemigrations -n ${n}

migrate:
	pipenv run python src/manage.py migrate ${o}

# Tests

test:
	cd src && pipenv run pytest --disable-warnings

unit:
	cd src && pipenv run pytest -m unit --disable-warnings

smoke:
	cd src && pipenv run pytest -m smoke --disable-warnings

integration:
	cd src && pipenv run pytest -m integration --disable-warnings


# Only dev management commands

initvacancies:
	pipenv run python src/manage.py initvacancies
