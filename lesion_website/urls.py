from django.urls import path

from lesion_website import views

urlpatterns = [
    path('lesion_website/', views.uploadPage, name="loadModel"),
    path('upload/<predicted_label>', views.resultsPage, name="uploadImage"),
    path('referral/', views.refferalPage, name="referral"),
    path('home/', views.homePage, name="homePage")
]
