from django.forms import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
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
# from .forms import ImageForm
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def uploadPage(request):
    new_model = load_model(
        os.path.join('C:\\Users\jesse\OneDrive\Desktop\Year 4\Project\models', 'model50epochs500resample64size.keras'))
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

            return redirect('uploadImage', predicted_label=predicted_label)

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

    return HttpResponse(template.render(context, request))


def loginPage(request):
    template = loader.get_template('login.html')
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homePage')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'login.html', context)


def registerPage(request):
    template = loader.get_template('register.html')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('loginPage')

    context = {'form': form}

    return render(request, 'register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('loginPage')

def refferalPage(request):
    from googleplaces import GooglePlaces, types, lang
    from django.http import JsonResponse
    import json
    from geopy.geocoders import Nominatim

    # calling the Nominatim tool
    loc = Nominatim(user_agent="GetLoc")

    # entering the location name
    getLoc = loc.geocode(" 28 Main Street Portlaoise")

    # printing address
    # print(getLoc.address)

    # printing latitude and longitude
    # print("Latitude = ", getLoc.latitude, "\n")
    # print("Longitude = ", getLoc.longitude)

    API_KEY = ('AIzaSyB3ZbQXl3kDtdlyFbhvJarw2-mXoFbh-2o')  # Google Maps API Key
    google_places = GooglePlaces(API_KEY)
    data = request.POST
    # Get the variables by their keys
    lat = data.get('data')
    lon = data.get('data2')

    # lat_lng = {'lat': 53.402040, 'lng': -6.407640}  # Replace with your latitude and longitude
    lat_lng = {'lat': getLoc.latitude, 'lng': getLoc.longitude}  # Replace with your latitude and longitude
    # numbers are none FIX THISSSSSSSSSSSS
    # lat_lng = {'lat': data_received, 'lng': data_received2}
    radius = 50000  # Radius in meters

    # Perform the nearby search for hospitals
    query_result = google_places.nearby_search(lat_lng=lat_lng, radius=radius, types=[types.TYPE_HOSPITAL])

    hospitalList = []

    # Print the results
    for place in query_result.places:
        place.get_details()

        s = ""
        if place.international_phone_number is not None:
            s = s + place.name + '\n' + place.international_phone_number + '\n' + place.url
            lines = s.split('\n')
            hospitalList.append(lines)

        # Create a dictionary with the hospitalList as the value
    context = {'hospitalList': hospitalList}

    # return HttpResponse(template.render(None,request))
    return render(request, 'refferal.html', context)
