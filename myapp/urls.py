from django.urls import path
from .views import index, contact, success, additional_works, meesho_ssrf_log

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('additional-projects/', additional_works, name='additional_works'),
    path('success/', success, name='success'),
    # SSRF Testing endpoint for Meesho vulnerability research
    path('meesho-log/', meesho_ssrf_log, name='meesho_ssrf_log'),
]
