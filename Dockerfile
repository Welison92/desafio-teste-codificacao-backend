FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir -p ./static

# Copiar todos os arquivos do projeto para /app
COPY . /app