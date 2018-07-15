from django.urls import path
from .views import CreateView, Logout, SetWeightRecord, CustomAuthToken, Register
from rest_framework.authtoken import views

urlpatterns = {
    path('getrecords', CreateView.as_view()),
    path('login', CustomAuthToken.as_view()),
    path('register', Register.as_view()),
    path('logout', Logout.as_view()),
    path('record', SetWeightRecord.as_view())
}
