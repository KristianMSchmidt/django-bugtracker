# Run development server
up:
	docker-compose up

# Rebuild development docker image
build:
	docker-compose build

# Rebuild development container and run development server
up-build:
	docker-compose up --build

# Execute all tests within the docker container
test:
	docker-compose run --rm web ./manage.py test

# Rebuild production docker image
build-prod:
	docker-compose -f docker-compose-prod.yml build

# Start docker production 
up-build-prod:
	docker-compose -f docker-compose-prod.yml up --build

# Open terminal within running docker development container
shell:
	docker-compose exec web /bin/bash

# Makemigrations within within docker container
migrations:
	docker-compose exec web python manage.py makemigrations

# Migrate within within docker container
migrate:
	docker-compose exec web python manage.py migrate

# Create superuser within docker container
superuser:
	docker-compose exec web python manage.py createsuperuser

# Deployment security checklist
check:
	docker-compose exec web python manage.py check --deploy

# Collect static (do this before every deployment to Heroku)
collectstatic:
	docker-compose exec web python manage.py collectstatic

# build production tailwind css & push master branch to heroku & check security
make push-heroku:
	git push heroku master
	heroku run python manage.py check --deploy

# Give myself ownership of all files in directory:
make chown:
	sudo chown -R $USER:$USER .
