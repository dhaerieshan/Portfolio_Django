from django.urls import path
from .views import index, contact, success

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('success/', success, name='success'),
]
