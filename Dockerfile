FROM python:slim-buster

WORKDIR /var/watcher

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY main.py main.py
COPY entrypoint.sh entrypoint.sh

CMD ["bash", "entrypoint.sh"]