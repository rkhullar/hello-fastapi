FROM python:3.8.11-alpine
WORKDIR /root
COPY Pipfile main.py ./
RUN pip install pipenv
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app"]
