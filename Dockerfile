FROM python:slim-buster

WORKDIR /var/watcher

CMD mkdir files

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY main.py main.py

CMD ["python3", "-u", "main.py"]