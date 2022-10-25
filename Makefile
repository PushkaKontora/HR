updev:
	docker-compose -f docker-compose.dev.yml up -d --build

downdev:
	docker-compose -f docker-compose.dev.yml down