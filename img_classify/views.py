from django.shortcuts import render
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings 
from tensorflow.python.keras.backend import set_session
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.models import load_model
import numpy as np
import datetime
import traceback
from PIL import Image
from numpy import asarray
import os
from img_classify.settings import MEDIA_ROOT#, model,train_generator

def index(request):
    if  request.method == "POST":
        f=request.FILES['sentFile'] # here you get the files needed
        response = {}
        file_name = "pic.jpg"
        file_name_2 = default_storage.save(file_name, f)

        img_width, img_height = 224,224
        img = load_img(os.path.join(MEDIA_ROOT, file_name_2), target_size=(img_width, img_height))

        x = img_to_array(img)
        x = x/255
        x = np.expand_dims(x, axis=0)

        images = np.vstack([x])

        model = load_model('model.h5')
        # model.compile(loss='binary_crossentropy',
        #       optimizer='rmsprop',
        #       metrics=['accuracy'])
        pred = model.predict(x)
        classes = np.array(pred)
        classes = np.where(classes > 0.5, 1, 0)
        label_map = {"cars":0,"planes":1}#(train_generator.class_indices)
        label_map = dict((v,k) for k,v in label_map.items())
        print("Lable map: ",label_map)
        print("model.predict(x): ",model.predict(x))
        print("classes: ",classes)

        predictions = [label_map[k] for k in classes[:,0]]

        if predictions[0]=="cars":
            prob = 1 - pred[0][0]
        else:
            prob = pred[0][0]

        
    
        response['name'] = f"Predicted class is : {predictions[0]} and the Probability of it being a {predictions[0]} is : {prob}"
        return render(request,'homepage.html',response)
    else:
        return render(request,'homepage.html')