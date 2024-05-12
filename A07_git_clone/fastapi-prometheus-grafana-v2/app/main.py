import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow
import uvicorn
from keras.models import load_model
from tensorflow.keras.models import Sequential
import numpy as np
from PIL import Image
import time
from fastapi import FastAPI, File, UploadFile, Query, Request, Response
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Gauge, start_http_server, generate_latest
import socket

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model, initialise to None
model = None

# Counters for tracking API usage from different client IP addresses
request_counter = Counter("api_requests_total", "Total API requests", ["client_ip"])

# Gauges for monitoring API runtime and processing time per character
api_runtime_gauge = Gauge("api_runtime_seconds", "API runtime in seconds")
processing_time_per_char_gauge = Gauge("processing_time_per_char_microseconds_SODA", "Processing time per character in microseconds", ["client_ip"])


# Function to get client IP
def get_client_ip():
    return socket.gethostbyname(socket.gethostname())

# Instrument your FastAPI application
Instrumentator().instrument(app).expose(app)

# Root endpoint
@app.get("/")
def home():
    return "Hii Hellooo Welcome to the Assignment by Sahil 😎😎😎"

# Predict digit function from last assignment
def predict_digit(model: Sequential, data_point: list) -> str:
    data_point = np.array(data_point).reshape(1, 784)
    prediction = model.predict(data_point)
    digit = str(np.argmax(prediction))
    return digit

# Format image function from last assignment
def format_image(file: UploadFile):
    image = Image.open(file.file)
    image = image.convert('L')
    image = image.resize((28, 28))
    data_point = list(image.getdata())
    return data_point

# Middleware to track request counts and runtime
# Note the usage of our custom Gauges and Counters
# This http endpoint is required by Prometheus to scrape metrics
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    api_runtime = time.time() - start_time
    api_runtime_gauge.set(api_runtime)
    processing_time_per_char_gauge.labels(client_ip=get_client_ip()).set(api_runtime / len(str(response)))
    request_counter.labels(client_ip=get_client_ip()).inc()
    return response


# Predict endpoint to make predictions an update the metrics and gauges
@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    start_time = time.time()
    data_point = format_image(file)
    if model is not None:
        digit = predict_digit(model, data_point)
        api_runtime = time.time() - start_time
        api_runtime_gauge.set(api_runtime)
        processing_time_per_char = (api_runtime / len(data_point)) * 1e6  # microseconds per character
        processing_time_per_char_gauge.labels(client_ip=get_client_ip()).set(processing_time_per_char)
        request_counter.labels(client_ip=get_client_ip()).inc()
        return {"digit": digit}
    else:
        return {"error": "Model not loaded. Please provide the model path."}


# Loading the model with a boundary validation check 
# for the presence of the model
@app.get("/load_model")
def load_model(model_path: str = Query(..., description="Path to the saved MNIST model")):
    global model
    try:
        model = tensorflow.keras.models.load_model(model_path)
        return {"message": "Model loaded successfully"}
    except ValueError:
        return {"error": "Keras model not found at the given path"}

# Metrics endpoint for prometheus that returns a Response variable
@app.get("/metrics")
async def get_metrics():
    return Response(content_type="text/plain", content=generate_latest())


# Start Prometheus metrics server
start_http_server(9090)
