FROM python:3.11

# WORKDIR /app/

# COPY . .

# RUN pip install -r requirements.txt

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD uvicorn --host=0.0.0.0 main:app --reload
