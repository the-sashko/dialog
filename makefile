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
	docker-compose build --no-cache

build-base:
	if [ -d ".build" ]; then rm -Rf .build; fi

	mkdir .build

	cp docker/python_setup/Dockerfile .build/Dockerfile
	cp requirements.txt .build/requirements.txt

	aws ecr get-login-password --region eu-west-2 --profile dialog-bot-deployment-user | docker login --username AWS --password-stdin 227900353800.dkr.ecr.eu-west-2.amazonaws.com

	cd .build; docker build -t the-sashko-dialog-bot-python .

	docker tag the-sashko-dialog-bot-python:latest 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot-python:latest

	docker push 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot-python:latest

	rm -rf .build
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
