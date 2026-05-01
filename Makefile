.PHONY: empty-db dev

dev:
	poetry run uvicorn server:app --reload



empty-db: data/wgo.local.db

data/wgo.local.db:
	poetry run python data/init_db.py

seed-local-data:
	sqlite3 data/wgo.local.db < data/seed_data.sql