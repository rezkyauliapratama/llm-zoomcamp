.PHONY: help setup ingest evaluate app monitoring clean

help:
	@echo "OJK AI Regulation Q&A — Available commands:"
	@echo "  make setup       Install dependencies"
	@echo "  make services    Start Docker services (ES, Grafana, PostgreSQL)"
	@echo "  make ingest      Run document ingestion pipeline"
	@echo "  make evaluate    Run RAG evaluation suite"
	@echo "  make app         Launch Streamlit app"
	@echo "  make clean       Stop and remove Docker services"

setup:
	pip install -r requirements.txt

services:
	docker-compose up -d

services-down:
	docker-compose down

ingest:
	python src/ingestion.py

evaluate:
	jupyter nbconvert --to notebook --execute notebooks/03-evaluation.ipynb

app:
	streamlit run app/app.py

monitoring:
	docker-compose -f monitoring/docker-compose.yml up -d

clean:
	docker-compose down -v
	docker-compose -f monitoring/docker-compose.yml down -v
