FROM python:3.8.12-alpine
WORKDIR /root
COPY Pipfile ./
RUN pip install pipenv                        \
    && pipenv lock                            \
    && pipenv requirements > requirements.txt \
    && pip install -r requirements.txt        \
    && rm requirements.txt
COPY fastapi ./
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
