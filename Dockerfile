FROM python:3.5

ENV PYTHONUNBUFFERED 1

ADD ./requirements.txt /requirements.txt

RUN mkdir /code

WORKDIR /code

ADD . /code/

RUN pip install -r requirements.txt

RUN groupadd -r django && useradd -r -g django django

RUN chown -R django /code
