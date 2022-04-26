FROM python:3.8

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update &&\
    apt install -y netcat

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod u+x entrypoint.sh

CMD ["sh", "entrypoint.sh"]