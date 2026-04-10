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


@require_http_methods(["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"])
def private_log(request, path=''):
    """
    Private logging endpoint - logs requests to console/file only.
    No public dashboard or views. Use for OAST testing.
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'method': request.method,
        'path': request.path,
        'full_path': request.get_full_path(),
        'headers': {k.replace('HTTP_', '').replace('_', '-'): v
                   for k, v in request.META.items() if k.startswith('HTTP_')},
        'body': request.body.decode('utf-8', errors='ignore') if request.body else None,
    }

    # Log to console (visible in Render logs)
    print(f"\n{'='*80}\n🔒 PRIVATE REQUEST LOGGED - {log_entry['method']} {log_entry['path']}\n{'='*80}")
    print(json.dumps(log_entry, indent=2, default=str))
    print(f"{'='*80}\n")

    # Also log to Django logger
    logger.info(f"Private Log: {log_entry['method']} {log_entry['full_path']}")

    return HttpResponse('OK', content_type='text/plain', status=200)
