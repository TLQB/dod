## Run container 
docker-compose build 
docker-compose up

## Migrate db
docker-compose run web python3 manage.py makemigrations
docker-compose run web python3 manage.py migrate