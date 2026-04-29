.PHONY: empty-db

empty-db: data/wgo.local.db

data/wgo.local.db:
	poetry run python data/init_db.py
