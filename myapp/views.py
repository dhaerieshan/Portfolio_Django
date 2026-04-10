from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
import json
import logging

from .forms import ContactForm

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'myapp/index.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            subject = f'Message from {name}'
            message = f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'
            from_email = settings.EMAIL_HOST_USER
            to_email = [settings.EMAIL_HOST_USER]

            try:
                send_mail(subject, message, from_email, to_email)
                return redirect('success')
            except Exception as e:
                print(f"Error sending email: {e}")

    else:
        form = ContactForm()

    return render(request, 'myapp/index.html', {'form': form})


def success(request):
    return render(request, 'myapp/success.html')


def additional_works(request):
    return render(request, 'myapp/additional_works.html')


@require_http_methods(["GET", "POST", "PUT", "DELETE", "HEAD"])
def meesho_ssrf_log(request):
    """
    SSRF Testing Endpoint - Logs all incoming requests for Meesho vulnerability testing
    Used for detecting Server-Side Request Forgery in profile_image endpoint
    """

    def get_client_ip(req):
        """Get client IP from request"""
        x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = req.META.get('REMOTE_ADDR')
        return ip

    # Extract request data
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'remote_ip': get_client_ip(request),
        'method': request.method,
        'path': request.path,
        'full_url': request.build_absolute_uri(),
        'headers': {k: v for k, v in request.META.items() if k.startswith('HTTP_')},
        'body': request.body.decode('utf-8', errors='ignore') if request.body else None,
    }

    # Log to console (visible in Render logs)
    print("\n" + "="*80)
    print("🚨 MEESHO SSRF TEST - INCOMING REQUEST 🚨")
    print("="*80)
    print(json.dumps(log_entry, indent=2, default=str))
    print("="*80 + "\n")

    # Also log to Django logger
    logger.info(f"SSRF Test Request: {json.dumps(log_entry, default=str)}")

    # Write to file (optional, for persistence)
    try:
        with open('meesho_requests.log', 'a') as f:
            f.write(json.dumps(log_entry, default=str) + '\n')
    except Exception as e:
        print(f"Error writing to log file: {e}")

    # Return fake PNG image so Meesho doesn't error on invalid image
    fake_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

    return HttpResponse(fake_png, content_type='image/png', status=200)
