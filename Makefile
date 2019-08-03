TARGET_DIR=blog
TAG=z0rr0/zblog

all: test

test:
	cd $(TARGET_DIR); python manage.py test posts.tests

static:
	mkdir -p $(TARGET_DIR)/posts/static
	mkdir -p $(TARGET_DIR)/posts/media
	cd $(TARGET_DIR); python manage.py collectstatic --no-input

prepare: static
	cd $(TARGET_DIR); python manage.py compilemessages -v2

docker: prepare
	docker build -t $(TAG) .
