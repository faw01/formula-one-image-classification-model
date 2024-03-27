from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import numpy as np

def initialize_model(path):
    data = tf.keras.utils.image_dataset_from_directory('/app/input/')
    class_names = data.class_names
    label_to_class = {i: class_name for i, class_name in enumerate(class_names)}
    return label_to_class, load_model(path)

label_to_class, model = initialize_model('/app/f1-racecar-image-classifier.h5')
app = FastAPI()

@app.post("/predict")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    if not file:
        return {"message": "No file sent"}
    else:
        image_np = np.frombuffer(file, np.uint8)
        img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)  
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        input_shape = (256, 256)
        resized_img = cv2.resize(img_rgb, input_shape)
        resized_img_normalized = resized_img / 255.0
        input_data = np.expand_dims(resized_img_normalized, axis=0)
        yhat = model.predict(input_data)
        sorted_indices = np.argsort(yhat[0])[::-1]
        prefixes = ['st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th', 'th']
        response = {
          'prediction': {
              'class': '',
              'confidence_percent': 0.0,
              'message': ''
          },
          'predictions': {}
        }
        for i, index in enumerate(sorted_indices):
            prob = yhat[0][index]
            class_name = label_to_class[index]
            message = f'{i+1}{prefixes[i]} Prediction: {class_name} with {prob*100:.2f}% confidence.'
            temp_dict = {
              'class': class_name,
              'confidence_percent': round(prob*100,2),
              'message': message
            }
            if i == 0:
                response['prediction'] = temp_dict
            response['predictions'][i+1] = temp_dict
        return response       

@app.get("/")
async def main():
    content = """
    <body>
    <h1>Formula 1 Image Classification Model</h1>
    <p> Choose a picture of a race car to upload in a form below</p>
    <form action="/predict" enctype="multipart/form-data" method="post">
    <input name="file" type="file">
    <input type="submit">
    </form>
    <a href="/healthcheck">Check API health</a>
    <p>Check API documentation: <a href="/docs">Swagger</a>, <a href="/redoc">ReDoc</a></p>
    </body>
    """
    return HTMLResponse(content=content)

@app.get("/healthcheck")
async def root():
    return {"message": "Hello World"}



