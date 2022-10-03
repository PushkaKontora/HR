dev:
	pipenv run python src/manage.py runserver

lint:
	pipenv run isort . & \
	pipenv run flake8 --config setup.cfg & \
	pipenv run black --config pyproject.toml .

check_lint:
	pipenv run isort --check --diff .
	pipenv run flake8 --config setup.cfg
	pipenv run black --check --config pyproject.toml .

migration:
	pipenv run python src/manage.py makemigrations -n ${n}

migrate:
	pipenv run python src/manage.py migrate ${o}
