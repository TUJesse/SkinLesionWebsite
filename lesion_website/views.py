import json

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
from django.contrib.auth.decorators import login_required
import requests


# Create your views here.

Latitude = None
Longitude = None
gotPost = False


def setLatLon(lat, lon):
    global Latitude
    global Longitude

    Latitude = lat
    Longitude = lon


@login_required(login_url='loginPage')
def CNN_SVM_UploadPage(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            img = request.FILES['image']
            files = {'file': img}

            #data = {'text': 'your_text_value'}

            api_url = 'http://127.0.0.1:5000/cnnsvm'
            response = requests.post(api_url, files=files)
            predicted_label = response.json()
            return redirect('uploadImage', predicted_label=predicted_label)

    elif request.method == 'GET':
        template2 = loader.get_template('CNNSVMImgUpload.html')
        context2 = {'form': ImageForm()}

        return HttpResponse(template2.render(context2, request))


@login_required(login_url='loginPage')
def preTrainedUploadPage(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            img = request.FILES['image']
            files = {'file': img}

            #data = {'text': 'your_text_value'}

            api_url = 'http://127.0.0.1:5000/prediction'
            response = requests.post(api_url, files=files)
            predicted_label = response.json()
            return redirect('uploadImage', predicted_label=predicted_label)

    elif request.method == 'GET':
        template2 = loader.get_template('preTrainedImgUpload.html')
        context2 = {'form': ImageForm()}

        return HttpResponse(template2.render(context2, request))



@login_required(login_url='loginPage')
def uploadPage(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            img = request.FILES['image']
            files = {'file': img}

            # data = {'text': 'your_text_value'}

            api_url = 'http://127.0.0.1:5000/pretrained'
            response = requests.post(api_url, files=files)
            predicted_label = response.json()
            return redirect('uploadImage', predicted_label=predicted_label)

    elif request.method == 'GET':
        template2 = loader.get_template('imgUpload.html')
        context2 = {'form': ImageForm()}

        return HttpResponse(template2.render(context2, request))


@login_required(login_url='loginPage')
def resultsPage(request, predicted_label):
    context = {'predicted_label': predicted_label}

    return render(request, 'lesion_upload.html', context)


@login_required(login_url='loginPage')
def homePage(request):
    template = loader.get_template('homePage.html')
    context = {'form': ImageForm()}

    return HttpResponse(template.render(context, request))


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('homePage')
    else:
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
    if request.user.is_authenticated:
        return redirect('homePage')
    else:
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

@login_required(login_url='loginPage')
def refferalPage(request):

    global Latitude
    if Latitude is None:
        return redirect('locationPage')

    from googleplaces import GooglePlaces, types, lang
    from django.http import JsonResponse
    import json
    from geopy.geocoders import Nominatim

    # calling the Nominatim tool
    loc = Nominatim(user_agent="GetLoc")

    # entering the location name
    #getLoc = loc.geocode(" 28 Main Street Portlaoise")

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
    lat_lng = {'lat': Latitude, 'lng': Longitude}  # Replace with your latitude and longitude
    # numbers are none FIX THISSSSSSSSSSSS
    # lat_lng = {'lat': data_received, 'lng': data_received2}
    radius = 5000  # Radius in meters

    # Perform the nearby search for hospitals
    query_result = google_places.nearby_search(lat_lng=lat_lng, radius=radius, types=[types.TYPE_HOSPITAL])

    hospitalList = []
    urlList = []
    zipped_list = []

    # Print the results
    for place in query_result.places:
        place.get_details()

        s = ""
        if place.international_phone_number is not None:
            s = s + str(place.name) + '\n' + str(place.international_phone_number)
            lines = s.split('\n')
            hospitalList.append(lines)
            urlList.append(str(place.url))

        zipped_list = zip(hospitalList, urlList)
        # Create a dictionary with the hospitalList as the value
    context = {'zipped_list': zipped_list}

    # return HttpResponse(template.render(None,request))
    return render(request, 'refferal.html', context)


@login_required(login_url='loginPage')
def locationPage(request):
    # context = {}
    # template = loader.get_template('getLocation.html')
    #gotPost = False
    #global gotPost

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        setLatLon(float(data.get('lat')), float(data.get('lon')))
        #gotPost = True

        print(f"Received data: {Latitude , Longitude}")
        #return redirect('referral')
    else:
        return render(request, 'getLocation.html')
        #return redirect('referral')

    # if gotPost:
    #     return redirect('referral')


def loadModelUp():
    model = keras.saving.load_model(os.path.join('C:\\Users\jesse\OneDrive\Desktop\Year 4\Project\models', 'Densenetmodel50epochs1500resample224size.keras'))
    return model