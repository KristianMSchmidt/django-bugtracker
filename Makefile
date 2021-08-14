# Run development server
up:
	docker-compose up

# Execute tests within the docker image
test:
	docker-compose run --rm web ./manage.py test

test-factories:
	docker-compose exec web python manage.py test tests.test_factories

test-forms:
	docker-compose exec web python manage.py test tests.test_forms

test-views:
	docker-compose exec web python manage.py test tests.test_views

# Rebuild development docker image
build:
	docker-compose build

# Rebuild production docker image
build-prod:
	docker-compose -f docker-compose-prod.yml build

# Start docker production 
build-up-prod:
	docker-compose -f docker-compose-prod.yml up --build


# Open terminal within running docker development container
terminal:
	docker-compose exec web /bin/bash

# Makemigrations within within docker image
migrations:
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


# build production tailwind css & push master branch to heroku & check security
make push-heroku:
	git push heroku master
	heroku run python manage.py check --deploy


# Open shell within running docker development container
shell:
	docker-compose exec web /bin/bash

# Collect static (do this before every deployment to Heroku)
collectstatic:
	docker-compose exec web python manage.py collectstatic