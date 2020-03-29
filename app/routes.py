#imports
from . import app
from flask import render_template, redirect, url_for, request, flash, jsonify
from datetime import datetime
import json
import base64
import numpy as np
import io, os
from PIL import Image
import keras
from keras import backend as K
from tensorflow.keras.models import load_model

#from keras.models import load_model
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array

import re
global model
model = None
#helper functions for the classification etc
def get_model():
    global model
    if model == None:
        print('Model Loaded')
        model = load_model(os.path.join(os.path.dirname(__file__),app.config['MODEL_NAME']))
        print('Model loading successful')

#preparing image
def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    return image



@app.route('/', methods=['GET'])
def index():
    #invoke function on script load
    get_model()
    return render_template("index.html")

@app.route('/locate-defects', methods=['POST'])
def predict_defects():
    
    data = request.get_json(force=True)
    raw_image = data['image']
    image_data = re.sub('^data:image/.+;base64,', '', raw_image)
    decoded_image =  base64.b64decode(image_data)
    dataBytes = io.BytesIO(decoded_image)
    image = Image.open(dataBytes)
    processed_image = preprocess_image(image, target_size=(128,128))

    prediction = model.predict(processed_image).tolist()

    print(prediction)
    response_dict = {
        "predictions":{
        },
        "raw": prediction
    }
    return jsonify({"Resp":response_dict})
