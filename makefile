include .env

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
	cp .env .build/.env
	cp docker-compose.yml .build/docker-compose.yml
	rm -rf .build/docker/python_setup

	rm -rf .build/data/download/*
	rm -rf .build/data/tmp/*

	rm -rf .build/data/logs/*

	if [ -f ".build/data/db.sqlite3" ]; then rm -rf .build/data/db.sqlite3; fi

	#cd .build && make parse
	rm .build/src/cron.py
	rm -rf .build/data/sources/*.txt
	rm -rf .build/data/sources/chats/*
	rm -rf .build/data/sources/*.txt
	rm -rf .build/data/sources/chats/*
	rm -rf .build/data/logs/*
	rm .build/makefile

	aws ecr get-login-password --region eu-west-2 --profile dialog-bot-deployment-user | docker login --username AWS --password-stdin 227900353800.dkr.ecr.eu-west-2.amazonaws.com

	cd .build && docker-compose build

	docker tag dialog-bot:latest 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot:${DIALOG_APP_VERSION}

	docker push 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot:${DIALOG_APP_VERSION}

	rm -rf .build

build-base:
	aws ecr get-login-password --region eu-west-2 --profile dialog-bot-deployment-user | docker login --username AWS --password-stdin 227900353800.dkr.ecr.eu-west-2.amazonaws.com

	docker build -t dialog-bot-python docker/python_setup/.

	docker tag dialog-bot-python:latest 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot-python:v0.1.0

	docker push 227900353800.dkr.ecr.eu-west-2.amazonaws.com/the-sashko-dialog-bot-python:v0.1.0

deploy:
	cd terraform && terraform validate
	cd terraform && terraform plan -var="app_version=${DIALOG_APP_VERSION}"
	cd terraform && terraform apply -auto-approve -var="app_version=${DIALOG_APP_VERSION}"

destroy:
	cd terraform && terraform destroy -auto-approve

run:
	@python3 src/app.py

cron:
	@rm -rf data/download/*
	@rm -rf data/tmp/*
	@python3 src/cron.py

