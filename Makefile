.PHONY: all env setupDependencies activateEnv up superuser

delete-none-image-docker:
	docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
req:
	pip freeze > requirements.txt
test:
	docker-compose run web python manage.py test
env:
	python3 -m venv .venv
setupDependencies:
	. .venv/bin/activate && pip install -r requirements.txt
up:
	docker-compose up
down:
	docker-compose down
superuser:
	docker-compose run web python manage.py createsuperuser
swagger:
	docker-compose run web python manage.py spectacular --file schema.yaml
clear:
	docker-compose down -v --rmi all