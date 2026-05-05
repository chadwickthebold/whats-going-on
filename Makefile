.PHONY: empty-db dev web-dev

dev:
	cd wgo-server && poetry run uvicorn server:app --reload

empty-db: wgo-server/data/wgo.local.db

wgo-server/data/wgo.local.db:
	cd wgo-server && poetry run python data/init_db.py

seed-local-data:
	sqlite3 wgo-server/data/wgo.local.db < wgo-server/data/seed_data.sql

web-dev:
	cd wgo-web-client && npm run dev