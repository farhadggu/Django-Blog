FROM python:alpine

# Install dependencies required for psycopg2 python package
RUN apk update && apk add libpq
RUN apk update && apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /code/

# Remove dependencies only required for psycopg2 build
RUN apk del .build-deps

# FROM python:alpine

# # Install dependencies required for psycopg2 python package
# RUN apk update && apk add libpq
# RUN apk update && apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

# WORKDIR /app

# COPY . /app

# RUN pip install --no-cache-dir -r requirements.txt

# # Remove dependencies only required for psycopg2 build
# RUN apk del .build-deps

# EXPOSE 8000

# CMD python manage.py createsuperuser --user admin --email admin@localhost --noinput;
