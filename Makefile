export POSTGRES_DB=postgres
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export DJANGO_SECRET_KEY=django-insecure-cbs+0uelf*4v0+9b3aw5!%^41xvs$^fj(ash_4cq^+k&\#7\#7m9

docker_compose=docker compose --project-directory ./ -f ./docker/docker-compose.yml

run:
	${docker_compose} --profile app up

pull:
	${docker_compose} pull

app_build:
	${docker_compose} --profile app build

seed:
	echo TODO

migrate:
	${docker_compose} --profile shell run --rm shell python manage.py migrate

migrations:
	${docker_compose} --profile shell run --rm shell python manage.py makemigrations

shell:
	${docker_compose} --profile shell run --rm shell python manage.py shell

test:
	echo TODO
