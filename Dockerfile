FROM python:3.12.10

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
