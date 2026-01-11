# --- Offline Pipelines ---

collect-crawl-data:
	uv run python -m tools.run --run-collect-crawl-data-pipeline

etl-pipeline:
	uv run python -m tools.run --run-etl-pipeline

compute-rag-pipeline:
	uv run python -m tools.run --run-compute-rag-pipeline