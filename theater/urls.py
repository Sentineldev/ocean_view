from django.urls import path

from . import views
from django.views import View

app_name = "theater"
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('prices/',views.PricesView.as_view(),name='prices'),
    path('board/',views.BoardView.as_view(),name='board'),
    path('functions/',views.FunctionsView.as_view(),name='functions'),
    path('premiere/',views.PremiereView.as_view(),name="premiere")
]