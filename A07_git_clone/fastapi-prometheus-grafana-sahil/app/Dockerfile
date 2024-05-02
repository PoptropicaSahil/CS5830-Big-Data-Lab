FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# CMD uvicorn --host=0.0.0.0 main:app

EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]

