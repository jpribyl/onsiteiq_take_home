export POSTGRES_DB=emeraldhouse
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=db
export POSTGRES_PORT=5432
export DJANGO_SECRET_KEY=django-insecure-cbs+0uelf*4v0+9b3aw5!%^41xvs$^fj(ash_4cq^+k&\#7\#7m9

docker_compose=docker compose --project-directory ./ -f ./docker/docker-compose.yml

.PHONY: help
.SILENT: help
help:	## print help message
	# https://stackoverflow.com/a/64996042
	@grep -Eh '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

.PHONY: run
run: ## Runs the dockerized application for development
	${docker_compose} --profile app up

.PHONY: pull
pull: ## Pulls docker containers
	${docker_compose} pull

.PHONY: app_build
app_build: ## Builds the app docker-compose profile
	${docker_compose} --profile app build

.PHONY: shell_build
shell_build: ## Builds the Django shell docker-compose profile
	${docker_compose} --profile shell build

.PHONY: seed
seed: ## Seeds the database with development data
	echo TODO

.PHONY: migrate
migrate: ## Runs Django migrations using `python manage.py migrate`
	${docker_compose} --profile shell run --rm shell python manage.py migrate

.PHONY: migrations
migrations: ## Analyzes Django model files for changes using `python manage.py makemigrations`
	${docker_compose} --profile shell run --rm shell python manage.py makemigrations

.PHONY: shell
shell: ## Drops the user into a Django shell using `python manage.py shell`
	${docker_compose} --profile shell run --rm shell python manage.py shell

.PHONY: bash
bash: ## Drops the user into a bash session on the docker container
	${docker_compose} --profile shell run --rm shell bash

.PHONY: pip_install
pip_install: ## Installs pip packages. Usage requires an argument of 'packages': `make pip_install packages="<some python package> <some other python package>"`
	${docker_compose} --profile shell run --rm shell bash -c 'pip install ${packages} && pip freeze > requirements.txt'

.PHONY: add_packages
add_packages: pip_install app_build shell_build ## Installs packages and rebuilds docker containers. Usage requires an argument of 'packages': `make add_packages packages="<some python package> <some other python package>"`

.PHONY: test
test: ## Runs the test suite using pytest
	echo TODO
