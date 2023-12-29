from django.forms import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from glob import glob
import seaborn as sns
from PIL import Image
from django.template import loader
from sklearn.metrics import confusion_matrix
import keras
import tensorflow as tf
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from scipy import stats
from sklearn.preprocessing import LabelEncoder
import cv2
from keras.models import load_model
from .forms import ImageForm

# Create your views here.
def uploadPage(request):
    new_model = load_model(os.path.join('C:\\Users\jesse\OneDrive\Desktop\Year 4\Project\models', 'model50epochs500resample64size.keras'))
    SIZE = 64
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES['image']

            image = Image.open(img)

            image = tf.image.resize(image, (SIZE, SIZE))
            image = np.expand_dims(image / 255, axis=0)
            prediction = new_model.predict(image)

            class_labels = ['Class 0 (akiec)', 'Class 1 (bcc)', 'Class 2 (bkl)', 'Class 3 (df)', 'Class 4 (mel)',
                            'Class 5 (nv)', 'Class 6 (vasc)']

            predicted_label = " " + class_labels[prediction.argmax()]

            return redirect('uploadImage',predicted_label= predicted_label)

    elif request.method == 'GET':
        template2 = loader.get_template('imgUpload.html')
        context2 = {'form': ImageForm()}

        return HttpResponse(template2.render(context2, request))

def resultsPage(request, predicted_label):
    context = {'predicted_label': predicted_label}

    return render(request, 'lesion_upload.html', context)

def homePage(request):
    template = loader.get_template('homePage.html')
    context = {'form': ImageForm()}

    return HttpResponse(template.render(context,request))

def refferalPage(request):
    template = loader.get_template('refferal.html')

    return HttpResponse(template.render(None,request))
