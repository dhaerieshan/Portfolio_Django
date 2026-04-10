from django.urls import path, re_path
from .views import index, contact, success, additional_works, private_log

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('additional-projects/', additional_works, name='additional_works'),
    path('success/', success, name='success'),

    # Private logging endpoint (no public views, logs to console only)
    path('private-log/', private_log, name='private_log'),
    re_path(r'^private-log/(?P<path>.*)$', private_log, name='private_log_with_path'),
]
