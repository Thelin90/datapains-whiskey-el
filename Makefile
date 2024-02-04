export APP := datapains/whiskey-extractor
export TAG := 0.0.1
export ENV := local

setup-environment: clean-environment install-environment install-linter

.PHONY: clean-environment
clean-environment:
	rm -rf build dist .eggs *.egg-info
	rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	find . -type d -name '.mypy_cache' -exec rm -rf {} +
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	find . -type f -name "*.py[co]" -exec rm -rf {} +

.PHONY: install-environment
install-environment:
	poetry env use 3.10
	poetry install

.PHONY: info-environment
info-environment:
	poetry env info
	poetry show --tree

.PHONY: test
test:
	poetry run python -m pytest tests/$(type)/ --cov-config=tests/$(type)/.coveragerc --cov=. --quiet $(test_argument)

.PHONY: update-environment
update-environment:
	poetry update

.PHONY: install-linter
install-linter:
	poetry run pre-commit clean
	poetry run pre-commit install

.PHONY: poetry-path
poetry-path:
	@echo $(shell eval poetry show -v 2> /dev/null | head -n1 | cut -d ' ' -f 3)

.PHONY: run
run:
	poetry run python run.py --config-file-name=$(config-file-name)

.PHONY: linter
linter:
	poetry run pre-commit run --all-files

.PHONY: run-container-linter
run-container-linter:
	docker run $(APP):$(TAG) make --directory app/ linter

.PHONY: build-container-image
build-container-image:
	docker build -t $(APP):$(TAG) -f tools/docker/Dockerfile .

.PHONY: get-container-info-environment
get-container-info-environment:
	docker run $(APP):$(TAG) make --directory app/ info-environment

.PHONY: delete-container-image
delete-container-image:
	docker rmi -f $(APP):$(TAG)

.PHONY: run-container-tests
run-container-tests:
	docker run $(APP):$(TAG) make --directory app/ test type=$(type)

.PHONY: exec-to-image
exec-to-image:
	docker run -it $(APP):$(TAG) bin/bash

.PHONY: apply-k8s
apply-k8s:
	kubectl apply -f tools/k8s/$(ENV)/$(LAYER)
