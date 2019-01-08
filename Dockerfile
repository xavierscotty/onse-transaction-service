FROM python:3.7.1-alpine

ADD . /app

WORKDIR /app

RUN pip install pipenv  && pipenv install --system

ENTRYPOINT ["python"]
CMD ["run.py"]