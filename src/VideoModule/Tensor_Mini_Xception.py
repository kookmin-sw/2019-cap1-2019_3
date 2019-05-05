import cv2
import numpy as np

from Oracle import Oracle

from keras.models import load_model
from keras.preprocessing.image import img_to_array

class Tensor_Mini_Xception(Oracle):
    def __init__(self, modelPath, faceClassifierPath):
        self.model = load_model(modelPath)
        self.face_cascade = cv2.CascadeClassifier(faceClassifierPath)

    def predict(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray_image, 1.3)#find position of faces

        result = []
        for (fX,fY,fW,fH) in faces:
            roi = gray_image[fY:fY + fH, fX:fX + fW]#cut face image
            roi = cv2.resize(roi, (48, 48))#resize to 48*48(classifier's input size)
            roi = roi.astype("float") / 255.0 #make gray scaler between 0~1
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            preds = self.model.predict(roi)
            result.append(preds)
        return result

    def predict_one(self, sliced_gray_image):
        preds = self.model.predict(sliced_gray_image)
        return preds


