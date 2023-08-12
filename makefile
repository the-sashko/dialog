default:
	@echo "Invalid target"

init:
	cp -r install/data data

	mkdir data/download
	mkdir data/logs
	mkdir data/tmp
	mkdir data/sources/chats

	chmod -R 775 data

	cd terraform && terraform init

	@echo "Done!"

build:
	if [ -d ".build" ]; then rm -rf .build; fi
	
	mkdir .build

	cp -r src .build/src
	cp -r data .build/data
	cp -r docker .build/docker
	cp makefile .build/makefile

	cd .build && make clean

	rm -rf .build/data/logs/*

	if [ -f ".build/data/db.sqlite3" ]; then rm -rf .build/data/db.sqlite3; fi

	cd .build && make parse

	rm -rf .build/data/sources/*.txt
	rm -rf .build/data/sources/chats/*
	rm -rf .build/data/logs/*

	aws ecr get-login-password --region eu-west-2 --profile dialog-bot-deployment-user | docker login --username AWS --password-stdin 227900353800.dkr.ecr.eu-west-2.amazonaws.com

	cd .build && docker-compose build

	docker tag dialog-bot:latest 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot:v0.0.1

	docker push 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot:v0.0.1

	rm -rf .build

build-base:
	aws ecr get-login-password --region eu-west-2 --profile dialog-bot-deployment-user | docker login --username AWS --password-stdin 227900353800.dkr.ecr.eu-west-2.amazonaws.com

	docker build -t dialog-bot-python docker/python_setup/.

	docker tag dialog-bot-python:latest 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot-python:v0.0.1

	docker push 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot-python:v0.0.1

deploy:
	cd terraform && terraform validate
	cd terraform && terraform plan
	cd terraform && terraform apply -auto-approve

destroy:
	cd terraform && terraform destroy -auto-approve

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
