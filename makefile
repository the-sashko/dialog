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

run:
	@python3 src/app.py

parse:
	@python3 src/markov_parseer.py

test:
	@echo "Done!"

dev:
	@echo "Done!"

cron:
	@echo "Done!"
