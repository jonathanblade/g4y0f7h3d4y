start:
	poetry run start

lint:
	poetry run mypy src

format:
	poetry run isort src
	poetry run black src

hooks:
	poetry run pre-commit run -a
