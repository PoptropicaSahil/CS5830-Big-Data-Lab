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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
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
    return "Hii Welcome to the final Project by Team Story 📖"


def load_model():
    global model
    try:
        model = pickle.load(open("./app/model.pkl", "rb"))
        return {"message": "Model loaded successfully"}
    except ValueError:
        return {
            "error": "Model could not be loaded, check if you are running the code from the XYZ directory"
        }


def format_data(file: UploadFile):
    # Save the uploaded file to a temporary directory
    # temp_file_path = os.path.join(os.getcwd(), file.filename)

    # script_run_logger.info(f"tmp file path is {temp_file_path}")

    # with open(temp_file_path, "wb") as temp_file:
    #     temp_file.write(await file.read())

    # script_run_logger.info("Created tmp file")

    # # Now you can read the saved file
    # data = pd.read_csv(temp_file_path, index_col=0)  # type: ignore
    # data = data.drop(["risk"], axis=1)

    # script_run_logger.info(f"data is {data}")

    # # Clean up the temporary file
    # os.remove(temp_file_path)

    data = pd.read_csv(file.file, index_col=0)  # type: ignore
    data = data.drop(["risk"], axis=1)
    ### WILL HAVE MANY MORE CHANGES LIKE
    # PREPROCESSING, NOT DROPPING TARGET COL, CHECK INDEX COL ETC

    return data


# @app.post("/upload")
# def upload_file(file: UploadFile = File(...)):
#     df = pd.read_csv(file.file)
#     file.file.close()
#     return {"filename": file.filename}


def predict_risk(model, data):

    # NOTE THAT I AM READING THE SAME FILE, THE LOGGER BELOW ALSO PRINTS THE EXPECTED DATA ONLY
    # data = pd.read_csv("./trial_data/sample.csv", index_col=0)
    # drop target col
    # data = data.drop(["risk"], axis=1)
    # print(data.columns)
    # script_run_logger.info(type(data))

    #############################
    # script_run_logger.info(f"predict risk function data is {data}")

    predictions = model.predict(data)  # type: ignore
    script_run_logger.info(f"predictions are {predictions}")

    return predictions


# Middleware to track request counts and runtime
# Note the usage of our custom Gauges and Counters
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


# Loading the model with a boundary validation check
# for the presence of the model
# @app.get("/load_model")
# def load_model(
#     model_path: str = Query(..., description="Path to the saved MNIST model"),
# ):
#     global model
#     try:
#         model = pickle.load(open("./app/model.pkl", "rb"))
#         return {"message": "Model loaded successfully"}
#     except ValueError:
#         return {"error": "Keras model not found at the given path"}


# Metrics endpoint for prometheus that returns a Response variable
@app.get("/metrics")
async def get_metrics():
    return Response(content_type="text/plain", content=generate_latest())  # type: ignore


# def og_function():
#     data = pd.read_csv("./trial_data/sample.csv", index_col=0)

#     # drop target col
#     data = data.drop(["risk"], axis=1)
#     # print(data.columns)

#     predictions = model.predict(data)

#     print(predictions)
#     return

# Start Prometheus metrics server
start_http_server(9090)
