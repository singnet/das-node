TARGETS=hyperon_das_node

build:
	@docker-compose build

up:
	@docker-compose up -d

down:
	@docker-compose down

restart:
	@docker-compose restart

logs:
	@docker-compose logs -f

elect_leader: # Manually starts a leader election
	@docker-compose run --rm start_election

build.determinant: # Build the Determinant example
	@docker-compose \
		-f ./hyperon_das_node/examples/determinant/docker-compose.yml \
		build
up.determinant: # Run the Determinant example
	@docker-compose \
		-f ./hyperon_das_node/examples/determinant/docker-compose.yml \
		up -d
start.determinant: # Starts the Determinant example
	@docker-compose \
		-f ./hyperon_das_node/examples/determinant/docker-compose.yml \
		run job_start

isort:
	@echo "Running isort"
	@poetry run isort $(TARGETS)

black:
	@echo "Running black"
	@poetry run black $(TARGETS)

flake8:
	@echo "Running flake8"
	@poetry run flake8 $(TARGETS)

mypy:
	@echo "Running mypy"
	@poetry run mypy $(TARGETS)

pylint:
	@echo "Running pylint"
	@poetry run pylint $(TARGETS)

lint: isort black flake8 pylint mypy
