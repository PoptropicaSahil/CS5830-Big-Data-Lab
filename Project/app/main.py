import os
import pickle
import socket
import sys
import time

import pandas as pd
from fastapi import FastAPI, File, Request, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Gauge, generate_latest, start_http_server
from prometheus_fastapi_instrumentator import Instrumentator

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.logging_config import script_run_logger

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


# Function to get client IP
def get_client_ip():
    return socket.gethostbyname(socket.gethostname())


# Instrument your FastAPI application
Instrumentator().instrument(app).expose(app)


# Root endpoint
@app.get("/")
def home():
    script_run_logger.info("started app and ran main page msg")
    return "Hii Welcome to the final Project by Team Story 📖📖"


def load_model():
    global model
    try:
        model = pickle.load(open("model.pkl", "rb"))
        return {"message": "Model loaded successfully"}
    except ValueError:
        return {
            "error": "Model could not be loaded, check if you are running the code from the XYZ directory"
        }


def format_data(file: UploadFile):

    data = pd.read_csv(file.file, index_col=0)  # type: ignore
    data = data.drop(["risk"], axis=1)
    ### WILL HAVE MANY MORE CHANGES LIKE
    # PREPROCESSING, NOT DROPPING TARGET COL, CHECK INDEX COL ETC

    return data


def predict_risk(model, data):
    predictions = model.predict(data)  # type: ignore
    script_run_logger.info(f"predictions are {predictions}")

    return predictions


# Middleware to track request counts and runtime
# This http endpoint is required by Prometheus to scrape metrics
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    api_runtime = time.time() - start_time
    api_runtime_gauge.set(api_runtime)
    request_counter.labels(client_ip=get_client_ip()).inc()
    return response


# Predict endpoint to make predictions an update the metrics and gauges
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    start_time = time.time()
    load_model()
    data = format_data(file)

    script_run_logger.info("loaded model and formatted data")
    script_run_logger.info(f"model type is {type(model)} and data type is {type(data)}")
    script_run_logger.info(f"data is {data}")

    if model is not None:
        risks = predict_risk(model, data)
        risks_list = risks.tolist()
        api_runtime = time.time() - start_time
        api_runtime_gauge.set(api_runtime)
        request_counter.labels(client_ip=get_client_ip()).inc()
        return {"risks": risks_list}
    else:
        return {"error": "Model not loaded. Please provide the model path."}



# Metrics endpoint for prometheus that returns a Response variable
@app.get("/metrics")
async def get_metrics():
    return Response(content_type="text/plain", content=generate_latest())  # type: ignore


# Start Prometheus metrics server
start_http_server(9090)
