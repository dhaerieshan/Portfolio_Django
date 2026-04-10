from django.urls import path
from .views import index, contact, success, additional_works

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('additional-projects/', additional_works, name='additional_works'),
    path('success/', success, name='success'),
]
