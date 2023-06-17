FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
#postgres client - for pg_restore
RUN apt-get update && apt-get install -y postgresql-client

COPY ./django_one/req.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./django_one /app

WORKDIR /app



COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

