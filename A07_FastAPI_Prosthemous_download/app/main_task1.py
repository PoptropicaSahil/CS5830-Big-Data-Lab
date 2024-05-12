# app/main.py
import os
import time
from fastapi import FastAPI
from prometheus_client import Counter, Gauge, start_http_server

from app.main_app import app as main_app

app = FastAPI()

REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['client_ip'])
REQUEST_TIME = Gauge('request_time', 'Time spent processing the request', ['client_ip'])
REQUEST_EFFICIENCY = Gauge('request_efficiency', 'Processing time per character', ['client_ip'])

start_http_server(8080)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    client_ip = request.client.host
    start_time = time.time()
    try:
        REQUEST_COUNT.labels(client_ip=client_ip).inc()
        response = await call_next(request)
        return response
    finally:
        duration = time.time() - start_time
        REQUEST_TIME.labels(client_ip=client_ip).set(duration)
        input_length = len(request.body())
        if input_length > 0:
            efficiency = duration / input_length * 1000000
            REQUEST_EFFICIENCY.labels(client_ip=client_ip).set(efficiency)

app.mount("/", main_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)