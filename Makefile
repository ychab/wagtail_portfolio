.DEFAULT_GOAL := help
.PHONY: help
.EXPORT_ALL_VARIABLES:

CURRENT_MAKEFILE := $(lastword $(MAKEFILE_LIST))

include .env

help:
	@LC_ALL=C $(MAKE) -pRrq -f $(CURRENT_MAKEFILE) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

confirm:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]

################
# Local command
################

deps:
	poetry show --outdated
	npm outdated

poetry:
	poetry update
	poetry lock
	poetry export -f requirements.txt --with prod -o requirements/prod.txt
	poetry export -f requirements.txt --with test -o requirements/test.txt
	poetry export -f requirements.txt --with test,dev -o requirements/dev.txt

npm:
	npm update
	npm run dist

precommit:
	pre-commit autoupdate

################
# Docker command
################

ps:
	docker compose ps --all

up:
	docker compose up --detach --wait

down:
	docker compose down --remove-orphans

down_clean:
	docker compose down --volumes --remove-orphans --rmi local

restart:
	docker compose restart

prune: confirm
	@# Be CAREFUL, would removed ALL unused stuff on your local machine!
	@# Be sure to have all your compose services RUNNING before executing it!
	docker system prune --all --force --volumes

reload: down up
reset: down_clean up

##############
# Docker utils
##############

dbshell:
	docker compose exec postgres psql -U ${PORTFOLIO_POSTGRES_USER} -d ${PORTFOLIO_POSTGRES_DB}

redisshell:
	docker compose exec redis redis-cli --user ${PORTFOLIO_REDIS_USER} -a ${PORTFOLIO_REDIS_PASSWORD}

redisflush:
	docker compose exec redis redis-cli --user ${PORTFOLIO_REDIS_USER} -a ${PORTFOLIO_REDIS_PASSWORD} flushall

###############
# Restore tools
###############

restore_media:
	scp ${PORTFOLIO_BACKUP_HOST}:${PORTFOLIO_BACKUP_PATH_MEDIA}/*.tgz .
	mv media media_old
	mv *.tgz latest.tar.gz
	tar xzf latest.tar.gz
	rm -Rf media_old latest.tar.gz

restore_db:
	# first fetch remote backup file.
	scp ${PORTFOLIO_BACKUP_HOST}:${PORTFOLIO_BACKUP_PATH_SQL}/*.sql.gz ./dump.sql.gz
	# Then stop any services and drop the DBs (postgres + redis)
	docker compose down --volumes
	# Then recreate the DB only (and wait for it's ready!)
	docker compose up --detach --wait postgres
	# Import the DUMP
	gunzip < dump.sql.gz | docker compose exec --no-TTY postgres psql --quiet -U ${PORTFOLIO_POSTGRES_USER} -d ${PORTFOLIO_POSTGRES_DB}
	# Cleanup the room!
	rm -f dump.sql.gz
	# Finally restart all services
	docker compose up --detach --wait

restore: restore_media restore_db
	python manage.py createadmin --password=admin
