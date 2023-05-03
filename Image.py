# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 22:51:30 2023

@author: Simanta Limbu
"""
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import base64
from PIL import Image as PILImage
import io
import os
import time
from ImageModel import Image
from flask_login import current_user
from User import db 

class ImageProcessor:
    
    @staticmethod
    def save_image_result(request, final_pred, user_id):
        filename = f"user_{user_id}_{int(time.time())}.jpg"
        file_path = os.path.join("saved_images", filename)
        file_path = file_path.replace('\\', '/')

      
         # Saving image with result text
        image = cv2.imread('static/after.jpg')
        cv2.putText(image, final_pred, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imwrite(os.path.join("static", file_path), image)  #

        # Saving image information to the database
        new_image = Image(file_path=file_path, result=final_pred, user_id=user_id)
        db.session.add(new_image)
        db.session.commit()
        
    @staticmethod
    def process_image(request):
        # Handling image taken from camera
        if 'camera_data' in request.form:
            data_url = request.form['camera_data']
            img_data = base64.b64decode(data_url[22:])
            img = PILImage.open(io.BytesIO(img_data))

            # Converting the image to RGB mode
            img = img.convert('RGB')

            # Saveing the image as JPEG
            img.save('static/file.jpg')

        # Handling uploaded image
        else:
            image = request.files['select_file']
            image = PILImage.open(image)
            
            image = image.convert('RGB')

            # Saving image to disk
            image.save('static/file.jpg')

        # Loading image using OpenCV
        image = cv2.imread('static/file.jpg')

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

        faces = cascade.detectMultiScale(gray, 1.1, 3)

        for x, y, w, h in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cropped = image[y:y+h, x:x+w]

        cv2.imwrite('static/after.jpg', image)

        try:
            cv2.imwrite('static/cropped.jpg', cropped)
        except:
            pass

        try:
            img = cv2.imread('static/cropped.jpg',0) 
        except:
            img = cv2.imread('static/file.jpg', 0)
       
        img = cv2.resize(img, (48,48))
        img = img/255
       
        img = img.reshape(1,48,48,1)
       
        model = load_model('model.h5')
       
        pred = model.predict(img)
       
        label_map = ['Anger','Neutral' , 'Fear', 'Happy', 'Sad', 'Surprise']
        pred = np.argmax(pred)
        final_pred = label_map[pred]
        
        
        return final_pred
