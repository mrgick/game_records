FROM python:3.11.2-slim

WORKDIR /game-records

COPY ./requirements.txt /game-records/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /game-records/requirements.txt

COPY ./app /game-records/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]