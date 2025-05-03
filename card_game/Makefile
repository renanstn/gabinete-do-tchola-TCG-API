clean:
	black --line-length 79 . && isort .

test:
	rm -f app.db
	python db_init.py
	pytest
