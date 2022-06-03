drop_db:
	psql -U postgres -c "DROP DATABASE portfolio_nelly"

create_db_user:
	psql -U postgres -c "CREATE USER portfolio_nelly WITH encrypted password 'portfolio_nelly' SUPERUSER"

create_db:
	psql -U postgres -c "CREATE DATABASE portfolio_nelly OWNER portfolio_nelly"

restore_db:
	psql -U postgres -d portfolio_nelly < backup.sql

admin:
	python manage.py createadmin --username=admin --password=admin

migrate:
	python manage.py migrate

start: create_db migrate admin

init: create_db_user start

reset: drop_db start

lint:
	pylama portfolio

sort:
	isort --check --diff portfolio

test:
	python manage.py test --settings=portfolio.settings.test --noinput portfolio

test_parallel:
	python manage.py test --settings=portfolio.settings.test --parallel=4 --noinput portfolio

test_fastfail:
	python manage.py test --settings=portfolio.settings.test --noinput --failfast portfolio

test_warn:
	python -Wd manage.py test --settings=portfolio.settings.test --noinput portfolio

test_reverse:
	python manage.py test --settings=portfolio.settings.test --reverse --parallel --noinput portfolio

test_report:
	coverage erase
	coverage run manage.py test --settings=portfolio.settings.test --no-input portfolio
	coverage report

test_html:
	coverage erase
	coverage run manage.py test --settings=portfolio.settings.test --no-input portfolio
	coverage html
