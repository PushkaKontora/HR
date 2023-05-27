FROM python:3.10-alpine3.17

WORKDIR /app

RUN apk update && \
    apk add make

COPY Pipfile* ./

RUN pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

COPY . .

CMD ["make", "migrate", "run"]