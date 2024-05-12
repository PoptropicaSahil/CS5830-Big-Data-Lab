# app/main_app.py
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow
import uvicorn
from fastapi import FastAPI, File, UploadFile
from keras.models import load_model
from tensorflow.keras.models import Sequential
import numpy as np
from PIL import Image
import argparse

app = FastAPI()

# Take the path of the model as a command line argument
parser = argparse.ArgumentParser()
parser.add_argument('--model_path', type=str, required=True, help='Path to the saved MNIST model')
args = parser.parse_args()

# load the model saved at the supply path on the disk
# and return the keras.src.engine.sequential.Sequential model
def load_model(path: str) -> Sequential:
    # Input boundary condition check if model is found
    try:
        return tensorflow.keras.models.load_model(path)
    except ValueError:
        raise Exception('Keras model not found at the given path, exiting...')
        exit()

# take the image serialized as an array of 784 elements
# and returns the predicted digit as string
def predict_digit(model: Sequential, data_point: list) -> str:
    data_point = np.array(data_point).reshape(1, 784)
    prediction = model.predict(data_point)
    digit = str(np.argmax(prediction))
    return digit

# resize any uploaded images to a 28x28 grey scale image
# followed by creating a serialized array of 784 elements
def format_image(file: UploadFile):
    image = Image.open(file.file)
    image = image.convert('L')  # Convert to grayscale
    image = image.resize((28, 28))
    data_point = list(image.getdata())
    return data_point

# read the bytes from the uploaded image to create an
# serialized array of 784 elements. The API endpoint
# returns {"digit":digit"} back to the client
@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    data_point = format_image(file)
    model = load_model(args.model_path)
    digit = predict_digit(model, data_point)
    return {"digit": digit}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)