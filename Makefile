.PHONY: test lint run deploy-lambda

test:
	pytest tests/ -v

lint:
	black src/ tests/
	flake8 src/ tests/

run:
	uvicorn src.main:app --reload

deploy-lambda:
	cd deployment/lambda && ./deployment_package.sh