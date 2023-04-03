version ?= latest

init-pre-commit:
	git config --global url."https://".insteadOf git://
	pre-commit install
	pre-commit run --all-files

build-docker-image:
	docker build -t daily-portrait:latest .

docker-run:
	docker run --rm -v `pwd`:/app daily-portrait:latest
