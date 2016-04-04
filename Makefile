pip-install: ## Install pinned packages from requirements.lock
	pip install -r requirements.lock

pip-update: ## Update packages from requirements.unlocked.txt
	pip install --upgrade -r requirements.unlocked.txt

pip-lock: ## Lock packages into requirements.lock
	pip freeze > requirements.lock

django-setup: ## Run initial local setup tasks
	cp --backup=numbered example.env .env

django-db-reset: ## Reset the database
	dropdb tor_councilmatic
	createdb tor_councilmatic

django-migrate: ## Run Django migrations
	python manage.py migrate --no-initial-data

django-loaddata: ## Load objects updated within the past 2 weeks
	$(eval MONTH_AGO := $(shell date --date='2 weeks ago' '+%F'))
	python manage.py loaddata --update_since $(MONTH_AGO)

heroku-deploy: ## Deploy to Heroku via git-push
	git push heroku master

heroku-pg-push: ## Push the tor_councilmatic DB to Heroku
	heroku pg:reset DATABASE
	heroku pg:push tor_councilmatic DATABASE

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
