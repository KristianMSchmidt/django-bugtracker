## ----------------------------------------------------------------------
## Makefile for bug-tracker-django.kristianms.com
##
## Used for both development and production. See targets below.
## ----------------------------------------------------------------------

help:   # Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

# ---------- Development ---------- #

up: ## Run development server
	docker-compose up

# Rebuild development docker image
build:
	docker-compose build

up-build: ## Rebuild development container and run development server
	docker-compose up --build

test: ## Execute all tests within the docker container
	docker-compose run --rm web ./manage.py test

shell: ## Open terminal within running docker development container
	docker-compose exec web /bin/bash

migrations: ## Makemigrations within within docker container
	docker-compose exec web python manage.py makemigrations

migrate: ## Migrate within within docker container
	docker-compose exec web python manage.py migrate


superuser: ## Create superuser within docker container
	docker-compose exec web python manage.py createsuperuser


check: ## Deployment security checklist
	docker-compose exec web python manage.py check --deploy

collectstatic: ## Collect static (do this before every deployment to Heroku)
	docker-compose exec web python manage.py collectstatic


# ---------- Production ---------- #
production_stop: ## Stop production server
	docker-compose -f docker-compose.prod.yml down --remove-orphans

production_start: ## Start production server as daemon
	docker-compose -f docker-compose.prod.yml up --build --remove-orphans -d

production_djangologs: ## Show django logs
	docker logs bug-tracker-django


production_traefiklogs: ## Show traefik access logs
	docker logs traefik


production_shell: # Open shell in running docker production container
	docker-compose -f docker-compose.prod.yml exec web /bin/bash


# ---------- Other ---------- #

make chown: ## Give myself ownership of all files in directory:
	sudo chown -R $USER:$USER .
