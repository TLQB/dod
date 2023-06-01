# pull official base image
FROM python:3.8.10-alpine

WORKDIR = /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip  
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod +x entrypoint.sh

COPY . .

# set the working directory to the app directory
WORKDIR /usr/src/app

# specify the command to run on container startup
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]