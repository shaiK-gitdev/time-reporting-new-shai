from django.urls import path
from . import views


urlpatterns = [  
    path('',views.getRoutes),
    path('forms/',views.getForms),
    path('forms/<str:pk>/',views.getForm),
]