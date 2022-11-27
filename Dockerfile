FROM serodioj/pypapi:6.0.0.1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app/ /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0"]
