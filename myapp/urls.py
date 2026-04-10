from django.urls import path, re_path
from .views import index, contact, success, additional_works, oast_log, oast_dashboard

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('additional-projects/', additional_works, name='additional_works'),
    path('success/', success, name='success'),

    # ===== OAST (Out-of-Band Application Security Testing) Endpoints =====
    # Generic logging endpoint - reusable for any app/vulnerability testing
    # Use any URL pattern and it will be logged

    # Dashboard to view all logged requests
    path('oast-dashboard/', oast_dashboard, name='oast_dashboard'),

    # Generic OAST logger - captures all HTTP requests
    # Examples:
    #   - https://your-domain.com/oast-log/ (basic log)
    #   - https://your-domain.com/oast-log/image.png (returns fake image)
    #   - https://your-domain.com/oast-log/script.js (returns fake JS)
    #   - https://your-domain.com/oast-log/style.css (returns fake CSS)
    #   - https://your-domain.com/oast-log/any/path/here (logs any path)
    path('oast-log/', oast_log, name='oast_log'),
    re_path(r'^oast-log/(?P<path>.*)$', oast_log, name='oast_log_with_path'),

    # Legacy aliases for compatibility
    path('meesho-log/', oast_log, name='meesho_log'),
    re_path(r'^meesho-log/(?P<path>.*)$', oast_log, name='meesho_log_with_path'),
]
