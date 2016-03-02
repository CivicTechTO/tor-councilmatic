pip-install: ## Install the pinned packages
	@pip install -r requirements.txt

pip-update: ## Update the packages
	@pip install --upgrade -r requirements.loose.txt

pip-lock: ## Lock the packages
	@pip freeze > requirements.txt

heroku-deploy: ## Deploy to Heroku via git-push
	@git push heroku toronto:master

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
