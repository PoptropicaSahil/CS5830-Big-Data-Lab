# Ensure consistent results from floating-point round-off errors from different computation orders
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow
import uvicorn
from fastapi import FastAPI, File, UploadFile
from keras.models import load_model
import numpy as np
from PIL import Image
import argparse

app = FastAPI()

# Task 1: Part 2
parser = argparse.ArgumentParser()
parser.add_argument('--model_path', type=str, required=True, help='Path to the saved MNIST model')
args = parser.parse_args()

# Task 1: Part 3
# def load_model(path: str):
#     return load_model(path)

def load_model(path: str):
    return tensorflow.keras.models.load_model(path)

# Task 1: Part 4
def predict_digit(model, data_point: list) -> str:
    data_point = np.array(data_point).reshape(1, 784)
    prediction = model.predict(data_point)
    digit = str(np.argmax(prediction))
    return digit

# Task 2: Part 1
def format_image(file: UploadFile):
    image = Image.open(file.file)
    image = image.convert('L')  # Convert to grayscale
    image = image.resize((28, 28))
    data_point = list(image.getdata())
    return data_point

# Task 1: Part 5
@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    # Task 2: Part 2
    data_point = format_image(file)
    model = load_model(args.model_path)
    digit = predict_digit(model, data_point)
    return {"digit": digit}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)