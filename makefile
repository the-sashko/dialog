default:
	@echo "Invalid target"

init:
	cp -r install/data data

	mkdir data/download
	mkdir data/logs
	mkdir data/tmp

	chmod -R 775 data

	@echo "Done!"

build:
	aws ecr get-login-password --region eu-west-2 --profile dialog-bot-deployment-user | docker login --username AWS --password-stdin 227900353800.dkr.ecr.eu-west-2.amazonaws.com

	docker-compose build

	docker tag dialog-bot:latest 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot:v0.0.1

	docker push 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot:v0.0.1

build-base:
	aws ecr get-login-password --region eu-west-2 --profile dialog-bot-deployment-user | docker login --username AWS --password-stdin 227900353800.dkr.ecr.eu-west-2.amazonaws.com

	docker build -t the-sashko-dialog-bot-python docker/python_setup/.

	docker tag the-sashko-dialog-bot-python:latest 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot-python:v0.0.1

	docker push 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot-python:v0.0.1

run:
	@python3 src/app.py

run-dev:
	@echo "Done!"

run-beta:
	@echo "Done!"

parse:
	@python3 src/markov_parseer.py

clean:
	@rm -rf data/download/*
	@rm -rf data/tmp/*

	@echo "Done!"
