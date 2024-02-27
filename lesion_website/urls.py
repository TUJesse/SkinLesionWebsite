from django.urls import path

from lesion_website import views

urlpatterns = [
    path('lesion_website/', views.uploadPage, name="loadModel"),
    path('densenet_model/', views.preTrainedUploadPage, name="densenetModel"),
    path('cnnsvm_model/', views.CNN_SVM_UploadPage, name="cnnSvmModel"),
    path('upload/<predicted_label>', views.resultsPage, name="uploadImage"),
    path('referral/', views.refferalPage, name="referral"),
    path('home/', views.homePage, name="homePage"),
    path('login/', views.loginPage, name="loginPage"),
    path('register/', views.registerPage, name="registerPage"),
    path('logout/', views.logoutUser, name="logoutPage")
]

