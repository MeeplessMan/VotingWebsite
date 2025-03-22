FROM python:3.13.2

RUN apt-get update && apt-get install --yes pipenv
WORKDIR /usr/src/dutsrcelections
ENV FLASK_APP=votingWebsite.py
COPY ./ /usr/src/dutsrcelections/
RUN pipenv install --deploy --ignore-pipfile
RUN flask db upgrade
RUN flask run