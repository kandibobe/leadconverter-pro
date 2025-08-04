.PHONY: format lint

format:
	black backend

lint:
	ruff check backend
