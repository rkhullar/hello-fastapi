FROM python:3.8.11-alpine
WORKDIR /root
COPY Pipfile main.py ./
RUN pip install pipenv                   \
    && pipenv lock -r > requirements.txt \
    && pip install -r requirements.txt   \
    && rm requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
