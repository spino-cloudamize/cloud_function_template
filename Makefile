SHELL=/usr/bin/env sh

ifndef CLOUD_FUNCTION
override CLOUD_FUNCTION=my_cloud_function
endif

##################################################
# Verbose & Log
#################################################
QUIET:=@
ifdef VERBOSE
	QUIET:=
endif

##################################################
# Rules
##################################################
.PHONY: help
help:
	@echo "Cloud Function template"
	@echo ""
	@echo "Do make [rule], where rule may be one of:"
	@echo "  - dev: installs dev dependencies in the virtualenv (pipenv)."
	@echo "  - requirements: generates the requirements.txt files."
	@echo "  - checks: run linters."
	@echo "  - test: run unittests."
	@echo "  - local: runs the cloud function locally"
	@echo "  - deploy_use_env: deploys cloud function passing secrets as env vars"

.PHONY: deploy_use_env
deploy_use_env:
	@echo Deploying using env vars
	gcloud functions deploy $(CLOUD_FUNCTION) --runtime python37 --trigger-http \
	--env-vars-file=env.yaml --entry-point entry_point

.PHONY: deploy_use_env
deploy_use_env:
	@echo Deploying using env vars
	gcloud functions deploy $(CLOUD_FUNCTION) --runtime python37 --trigger-http \
	--env-vars-file=env.yaml --entry-point entry_point

.PHONY: dev
dev: 
	@echo Installing dev dependencies 
	pipenv install --dev
	pipenv run pip install -e .

.PHONY: requirements
requirements:
	@echo "Writting requirement files..."
	pipenv run pipenv_to_requirements -f

.PHONY: checks
checks: flake8 pylint

.PHONY: flake8
flake8:
	@echo "flake8: Linting files..."
	- pipenv run flake8 ./

.PHONY: pylint
pylint:
	@echo "pylint: Linting files..."
	- pipenv run pylint --rcfile=.pylintrc --output-format=colorized ./helpers *.py

.PHONY: test
test:
	@echo "Running test cases..."
	- pipenv run pytest -v --rootdir=tests $(TESTS)

.PHONY: local
local:
	@echo "Running locally..."
	- pipenv run ./run_local.sh