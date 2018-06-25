from django.urls import path
from .views import CreateView, Logout, SetWeightRecord
from rest_framework.authtoken import views

urlpatterns = {
    path('getrecords/', CreateView.as_view()),
    path('login/', views.obtain_auth_token),
    path('logout/', Logout.as_view()),
    path('record/', SetWeightRecord.as_view())
}
