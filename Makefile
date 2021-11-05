.SILENT: fmt check lint

fmt:
	autoflake \
		--in-place \
		--remove-all-unused-imports \
		--ignore-init-module-imports \
		-r \
		codemods tests
	isort --profile black .
	black .

check:
	autoflake \
		--in-place \
		--remove-all-unused-imports \
		--ignore-init-module-imports \
		-r \
		-c \
		codemods tests
	isort --profile black -c .
	black --check .

lint:
	mypy codemods tests
	flake8 .

test:
	pytest -x --cov=codemods --cov-fail-under=90
