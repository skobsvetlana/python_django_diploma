FROM python:3.10.0

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==1.8.2"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY diploma-frontend .
COPY mysite .

RUN pip install "diploma-frontend/dist/diploma-frontend-0.6.tar.gz"

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
