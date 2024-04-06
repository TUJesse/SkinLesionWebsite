import json
import os

import keras
import numpy as np
import pandas as pd
import plotly.express as px
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from geopy.geocoders import Nominatim
from googleplaces import GooglePlaces, types

# from .forms import ImageForm
from .forms import *

# Create your views here.

Latitude = None
Longitude = None
gotPost = False
LesionImg = None

def setLatLon(lat, lon):
    global Latitude
    global Longitude

    Latitude = lat
    Longitude = lon


#@login_required(login_url='loginPage')
def CNN_SVM_UploadPage(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            global LesionImg
            img = request.FILES['image']
            LesionImg = img.read()
            files = {'file': (img.name, LesionImg)}

            #data = {'text': 'your_text_value'}

            #api_url = 'http://127.0.0.1:5000/cnnsvm'
            api_url = 'https://lesion-api-2yllx.ondigitalocean.app/cnnsvm'
            response = requests.post(api_url, files=files, timeout=120)
            predicted_label = response.json()
            return redirect('uploadImage', predicted_label=predicted_label)
        else:
            template2 = loader.get_template('CNNSVMImgUpload.html')
            context2 = {'form': ImageForm(), 'errorMsg': 'Please upload supported image file format (jpg, jpeg)'}

            return HttpResponse(template2.render(context2, request))

    elif request.method == 'GET':
        template2 = loader.get_template('CNNSVMImgUpload.html')
        context2 = {'form': ImageForm()}

        return HttpResponse(template2.render(context2, request))


#@login_required(login_url='loginPage')
def preTrainedUploadPage(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            global LesionImg
            img = request.FILES['image']
            LesionImg = img.read()
            files = {'file': (img.name, LesionImg)}

            #data = {'text': 'your_text_value'}

            api_url = 'https://lesion-api-2yllx.ondigitalocean.app/prediction'
            #api_url = 'http://127.0.0.1:5000/prediction'
            response = requests.post(api_url, files=files, timeout=120)
            predicted_label = response.json()
            return redirect('uploadImage', predicted_label=predicted_label)
        else:
            template2 = loader.get_template('preTrainedImgUpload.html')
            context2 = {'form': ImageForm(), 'errorMsg': 'Please upload supported image file format (jpg, jpeg)'}

            return HttpResponse(template2.render(context2, request))

    elif request.method == 'GET':
        template2 = loader.get_template('preTrainedImgUpload.html')
        context2 = {'form': ImageForm()}

        return HttpResponse(template2.render(context2, request))


#@login_required(login_url='loginPage')
def uploadPage(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            global LesionImg
            img = request.FILES['image']
            LesionImg = img.read()
            files = {'file': (img.name, LesionImg)}

            # data = {'text': 'your_text_value'}

            #api_url = 'http://127.0.0.1:5000/pretrained'
            #api_url = 'https://lesion-apis.onrender.com/pretrained'
            api_url = 'https://lesion-api-2yllx.ondigitalocean.app/pretrained'
            response = requests.post(api_url, files=files)
            predicted_label = response.json()

            return redirect('uploadImage', predicted_label=predicted_label)
        else:
            template2 = loader.get_template('imgUpload.html')
            context2 = {'form': ImageForm(), 'errorMsg': 'Please upload supported image file format (jpg, jpeg)'}

            return HttpResponse(template2.render(context2, request))

    elif request.method == 'GET':
        template2 = loader.get_template('imgUpload.html')
        context2 = {'form': ImageForm()}

        return HttpResponse(template2.render(context2, request))


#@login_required(login_url='loginPage')
def resultsPage(request, predicted_label):
    global LesionImg
    chart = plotImg(LesionImg)
    context = {'predicted_label': predicted_label, 'chart': chart}

    return render(request, 'lesion_upload.html', context)


#@login_required(login_url='loginPage')
def homePage(request):
    template = loader.get_template('index.html')
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
    # if request.user.is_authenticated:
    #     return redirect('homePage')
    # else:
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

#@login_required(login_url='loginPage')
def refferalPage(request):

    global Latitude
    if Latitude is None:
        return redirect('locationPage')

    # calling the Nominatim tool
    loc = Nominatim(user_agent="GetLoc")


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


#@login_required(login_url='loginPage')
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

def plotImg(img):
    import cv2

    #image_data = img.read()
    image = np.frombuffer(img, np.uint8)

    # load image
    #imageObj = cv2.imread(img)
    imageObj = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # Get RGB data from image
    blue_color = cv2.calcHist([imageObj], [0], None, [256], [0, 256]).flatten()
    red_color = cv2.calcHist([imageObj], [1], None, [256], [0, 256]).flatten()
    green_color = cv2.calcHist([imageObj], [2], None, [256], [0, 256]).flatten()

    # Create DataFrame
    histogram_data = {
        'Intensity': np.arange(256),
        'Blue': blue_color,
        'Green': green_color,
        'Red': red_color
    }
    df = pd.DataFrame(histogram_data)

    # Plot histogram using Plotly Express
    fig = px.line(df, x='Intensity', y=['Blue', 'Green', 'Red'], title='Histogram of RGB Colors of the Lesion image')
    return fig.to_html()