# Variables
APP_NAME = HackerNewsClone

#====================================
#== PYTHON DJANGO ENVIRONMENT Targets
#====================================

PYTHON = @python

makemigrations:
	${PYTHON} manage.py makemigrations

migrate:
	${PYTHON} manage.py migrate

start-server:
	${PYTHON} manage.py runserver

createsuperuser:
	${PYTHON} manage.py createsuperuser

update-app: makemigrations migrate start-server


#====================================
#===== DOCKER ENVIRONMENT Targets
#====================================