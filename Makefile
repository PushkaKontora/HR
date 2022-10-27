# Dev

updev:
	docker-compose -f docker-compose.dev.yml up -d --build

downdev:
	docker-compose -f docker-compose.dev.yml down

builddev:
	docker-compose -f docker-compose.dev.yml build

testdev:
	docker-compose -f docker-compose.dev.yml run api make test

checkdev:
	docker-compose -f docker-compose.dev.yml run api make check