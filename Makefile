# You must export these environment variables before using remote restore.
BACKUP_HOST=$(PORTFOLIO_NELLY_BACKUP_HOST)
BACKUP_PATH_SQL=$(PORTFOLIO_NELLY_BACKUP_PATH_SQL)
BACKUP_PATH_MEDIA=$(PORTFOLIO_NELLY_BACKUP_PATH_MEDIA)

all:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

help: all

check_deps:
	poetry show --outdated

poetry:
	poetry update
	poetry lock
	poetry export -f requirements.txt --only main -o requirements/prod.txt
	poetry export -f requirements.txt --with test -o requirements/test.txt
	poetry export -f requirements.txt --with test,dev -o requirements/dev.txt

drop_db:
	psql -U postgres -c "DROP DATABASE portfolio_nelly"

create_db_user:
	psql -U postgres -c "CREATE USER portfolio_nelly WITH encrypted password 'portfolio_nelly' SUPERUSER"

create_db:
	psql -U postgres -c "CREATE DATABASE portfolio_nelly OWNER portfolio_nelly"

restore_db:
	scp ${BACKUP_HOST}:${BACKUP_PATH_SQL}/*.sql.gz .
	gunzip *.sql.gz
	mv *.sql latest.sql
	psql -U postgres -d portfolio_nelly < latest.sql
	python manage.py createadmin --username=admin --password=admin --update
	python manage.py updatesite --hostname=127.0.0.1 --port 8000
	rm -f *.sql

restore_media:
	scp ${BACKUP_HOST}:${BACKUP_PATH_MEDIA}/*.tgz .
	mv media media_old
	mv *.tgz latest.tar.gz
	tar xvzf latest.tar.gz
	rm -Rf media_old latest.tar.gz

restore: drop_db create_db restore_db restore_media

migrate:
	python manage.py migrate

admin:
	python manage.py createadmin --username=admin --password=admin

reset: drop_db create_db migrate admin
