FROM python:3.10.5

WORKDIR /usr/src/app

COPY ./* ./

COPY ./app/* ./app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", " app.main.:app", "--host", "0.0.0.0", "--port", "8080"]