delete-none-image-docker:
	docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
req:
	pip freeze > requirements.txt
test:
	docker-compose run web python manage.py test