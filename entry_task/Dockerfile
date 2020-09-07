FROM python:2.7.17

WORKDIR /entry_task

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev  -y

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod 755 ./wait-for-it.sh
CMD ["python"]