from django.urls import path
from . import views

urlpatterns = [

    path('', views.home_page, name='home_page'),
    path('routes/', views.return_routes, name='return_routes'),
]
