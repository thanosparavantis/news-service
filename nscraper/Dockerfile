FROM python:3.12-slim as base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY ./src/nscraper /app/nscraper
COPY ./firebase.json /app/firebase.json
COPY ./requirements.txt /app/requirements.txt
COPY ./run_loop.py /app/run_loop.py
WORKDIR /app
RUN python -m pip install -r requirements.txt
CMD python run_loop.py
