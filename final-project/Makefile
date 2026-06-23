.PHONY: up down ingest eval app

up:
	docker-compose -f docker/docker-compose.yml up -d

down:
	docker-compose -f docker/docker-compose.yml down

ingest:
	python pipeline/ingestion_pipeline.py

eval:
	python -m pytest src/evaluation/ -v

app:
	streamlit run app/app.py

lint:
	ruff check src/ app/ pipeline/
