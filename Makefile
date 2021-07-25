# Run development server
runserver:
	docker-compose up

# Execute tests within the docker image
test:
	docker-compose run --rm web ./manage.py test

# Rebuild development docker image
build:
	docker-compose build

# Rebuild production docker image
build-prod:
	docker-compose -f docker-compose-prod.yml build

# Start docker
up:
	docker-compose up

# Start docker production 
build-up-prod:
	docker-compose -f docker-compose-prod.yml up --build


# Open shell within running docker development container
shell:
	docker-compose exec web /bin/bash

# Makemigrations within within docker image
migrate:
	docker-compose exec web python manage.py makemigrations

# Migrate within within docker image
migrate:
	docker-compose exec web python manage.py migrate

# Create superuser within docker
superuser:
	docker-compose exec web python manage.py createsuperuser

# Deployment security checklist
check:
	docker-compose exec web python manage.py check --deploy

# Generate new secret key
secret:
	docker-compose exec web python -c 'import secrets; print(secrets.token_urlsafe(38))'

