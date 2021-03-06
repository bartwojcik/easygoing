FROM python:3.6
RUN apt-get update && apt-get install -y \
 libz-dev \
 libjpeg-dev \
 libfreetype6-dev \
 python-dev \
 postgresql-client \
 gettext
RUN groupadd -r user && useradd -r -g user user
RUN chmod 1777 /tmp
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install --upgrade pip --no-cache-dir &&\
    pip install -r requirements.txt --no-cache-dir
COPY . /code/
ENV DEBUG 1
RUN python manage.py compilemessages
ENV DEBUG 0