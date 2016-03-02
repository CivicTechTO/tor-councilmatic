pip-install: ## Install pinned packages from requirements.lock
	@pip install -r requirements.lock

pip-update: ## Update packages from requirements.unlocked.txt
	@pip install --upgrade -r requirements.unlocked.txt

pip-lock: ## Lock packages into requirements.lock
	@pip freeze > requirements.lock

heroku-deploy: ## Deploy to Heroku via git-push
	@git push heroku toronto:master

heroku-pg-push: ## Push the tor_councilmatic DB to Heroku
	@heroku pg:push tor_councilmatic DATABASE

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
