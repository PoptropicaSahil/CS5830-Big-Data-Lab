# We set this environment variable to 0 to 
# ensure consistent results from floating-point round-off errors
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

import tensorflow
import uvicorn
# from fastapi import FastAPI, File, UploadFile
from fastapi import FastAPI, File, UploadFile, Query
from keras.models import load_model
from tensorflow.keras.models import Sequential
import numpy as np
from PIL import Image
# import argparse

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
model = None


@app.get("/")
def home():
    return "Hii Hellooooo World lihas liao liao TIAAA "



# app = FastAPI()

# Task 1: Part 2
# Take the path of the model as a command line argument
# parser = argparse.ArgumentParser()
# parser.add_argument('--model_path', type=str, required=True, help='Path to the saved MNIST model')
# args = parser.parse_args()

# Task 1: Part 3
# load the model saved at the supply path on the disk 
# and return the keras.src.engine.sequential.Sequential model
# def load_model(path: str) -> Sequential:
#     # Input boundary condition check if model is found
#     try :
#         return tensorflow.keras.models.load_model(path)
#     except ValueError: 
#         raise Exception('Keras model not found at the given path, exiting...')
#         exit()

# Task 1: Part 4
# take the image serialized as an array of 784 elements
# and returns the predicted digit as string
def predict_digit(model: Sequential, data_point: list) -> str:
    data_point = np.array(data_point).reshape(1, 784)
    prediction = model.predict(data_point)
    digit = str(np.argmax(prediction))
    return digit

# Task 2: Part 1
# resize any uploaded images to a 28x28 grey scale image
# followed by creating a serialized array of 784 elements
def format_image(file: UploadFile):
    image = Image.open(file.file)
    image = image.convert('L')  # Convert to grayscale
    image = image.resize((28, 28))
    data_point = list(image.getdata())
    return data_point

# Task 1: Part 5
# read the bytes from the uploaded image to create an 
# serialized array of 784 elements. The API endpoint
# returns {“digit”:digit”} back to the client
# @app.post('/predict')
# async def predict(file: UploadFile = File(...)):
#     # Task 2: Part 2
#     # incorporate “format_image” inside the “/predict” endpoint
#     data_point = format_image(file)
#     # print(f'model path read is {args.model_path}')
#     # model = load_model(args.model_path)
#     digit = predict_digit(model, data_point)
#     return {"digit": digit}


@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    # Task 2: Part 2
    # incorporate "format_image" inside the "/predict" endpoint
    data_point = format_image(file)
    if model is not None:
        digit = predict_digit(model, data_point)
        return {"digit": digit}
    else:
        return {"error": "Model not loaded. Please provide the model path."}
    
# Load the model based on the provided model path
# @app.on_event("startup")
# def load_model(model_path: str = Query(..., description="Path to the saved MNIST model")):
#     global model
#     # ... (your existing code to load the model goes here)
#         # Input boundary condition check if model is found
#     try :
#         # model =  tensorflow.keras.models.load_model(model_path)
#         model =  tensorflow.keras.models.load_model(model_path)
#     except ValueError: 
#         raise Exception('Keras model not found at the given path, exiting...')
#         exit()
    # model =  tensorflow.keras.models.load_model(model_path)

    # model = load_model(model_path)

# Load the model based on the provided model path
@app.get("/load_model")
def load_model(model_path: str = Query(..., description="Path to the saved MNIST model")):
    global model
    try:
        model = tensorflow.keras.models.load_model(model_path)
        return {"message": "Model loaded successfully"}
    except ValueError:
        return {"error": "Keras model not found at the given path"}
    
# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8000)



Instrumentator().instrument(app).expose(app)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
