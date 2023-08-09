default:
	@echo "Invalid target"

install:
	cp -r install/data data

	mkdir data/download
	mkdir data/logs
	mkdir data/tmp

	chmod -R 775 data

	@echo "Done!"

run:
	@python3 src/app.py

test:
	@echo "Done!"

dev:
	@echo "Done!"

cron:
	@echo "Done!"
