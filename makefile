install:
	pip install -r requirements.txt
migrations:
	python manage.py makemigrations
	python manage.py migrate
seed:
	python manage.py seed_db
test:
	pytest -v -rP
run:
	python manage.py runserver
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete