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
def oast_log(request, path=''):
    """
    Generic OAST (Out-of-Band Application Security Testing) Logging Endpoint
    Logs ALL incoming requests - reusable for any app vulnerability testing
    Supports: SSRF, SSRFP, callback testing, webhook testing, etc.

    Usage: Set any URL to point here, endpoint logs and returns fake response
    """

    def get_client_ip(req):
        """Extract real client IP (handles proxies)"""
        x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = req.META.get('REMOTE_ADDR')
        return ip

    # Extract everything
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'remote_ip': get_client_ip(request),
        'method': request.method,
        'path': request.path,
        'full_path': request.get_full_path(),
        'query_params': dict(request.GET),
        'headers': {k.replace('HTTP_', '').replace('_', '-'): v for k, v in request.META.items() if k.startswith('HTTP_')},
        'content_type': request.META.get('CONTENT_TYPE'),
        'body': request.body.decode('utf-8', errors='ignore') if request.body else None,
        'cookies': dict(request.COOKIES),
    }

    # Print to console (Render logs)
    print("\n" + "="*100)
    print(f"🚨 OAST REQUEST CAPTURED - {log_entry['method']} {log_entry['path']}")
    print("="*100)
    print(json.dumps(log_entry, indent=2, default=str))
    print("="*100 + "\n")

    # Log to Django logger
    logger.info(f"OAST Request: {log_entry['method']} {log_entry['full_path']} from {log_entry['remote_ip']}")

    # Persist to file
    try:
        import os
        log_file = 'oast_requests.log'
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry, default=str) + '\n')
    except Exception as e:
        logger.error(f"Error writing to log file: {e}")

    # Return appropriate response based on request type
    file_extension = path.split('.')[-1].lower() if path else ''

    # Image file
    if file_extension in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
        fake_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        return HttpResponse(fake_png, content_type='image/png', status=200)

    # JSON request
    elif 'json' in request.META.get('CONTENT_TYPE', ''):
        return HttpResponse(json.dumps({'status': 'logged', 'timestamp': log_entry['timestamp']}),
                          content_type='application/json', status=200)

    # CSS file
    elif file_extension == 'css':
        return HttpResponse('body { color: red; }', content_type='text/css', status=200)

    # JavaScript file
    elif file_extension == 'js':
        return HttpResponse('console.log("OAST");', content_type='application/javascript', status=200)

    # HTML
    elif file_extension in ['html', 'htm'] or 'text/html' in request.META.get('ACCEPT', ''):
        html = '''<!DOCTYPE html>
        <html>
        <head><title>OAST</title></head>
        <body>
            <h1>Request Logged</h1>
            <p>This OAST endpoint has logged your request.</p>
            <script>
                // Attempt to exfiltrate data
                fetch('/oast-dashboard/');
            </script>
        </body>
        </html>'''
        return HttpResponse(html, content_type='text/html', status=200)

    # Default: plain text
    else:
        return HttpResponse(f'OAST: Request logged at {log_entry["timestamp"]}',
                          content_type='text/plain', status=200)


def oast_dashboard(request):
    """
    Dashboard to view all logged OAST requests
    Shows last 50 requests with filtering/search
    """

    requests_list = []
    filter_ip = request.GET.get('ip', '')
    filter_method = request.GET.get('method', '')
    search_query = request.GET.get('search', '')

    try:
        with open('oast_requests.log', 'r') as f:
            lines = f.readlines()
            # Read last 100 entries
            for line in lines[-100:]:
                try:
                    entry = json.loads(line.strip())

                    # Apply filters
                    if filter_ip and filter_ip not in entry.get('remote_ip', ''):
                        continue
                    if filter_method and filter_method != entry.get('method', ''):
                        continue
                    if search_query and search_query not in json.dumps(entry):
                        continue

                    requests_list.append(entry)
                except:
                    pass
    except FileNotFoundError:
        pass

    # Reverse to show newest first
    requests_list.reverse()

    # Build request cards HTML
    requests_html = "".join([f'''
        <div class="request">
            <div class="timestamp">{req['timestamp']}</div>
            <div class="ip">IP: {req['remote_ip']}</div>
            <div class="method">METHOD: {req['method']}</div>
            <div class="path">PATH: {req['path']}</div>
            <div class="json"><pre>{json.dumps(req, indent=2)}</pre></div>
        </div>
        ''' for req in requests_list[:50]])

    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>OAST Dashboard - Security Testing Logs</title>
        <style>
            body {{ font-family: monospace; margin: 20px; background: #1e1e1e; color: #00ff00; }}
            .header {{ background: #333; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
            .filters {{ margin: 20px 0; }}
            input {{ padding: 8px; background: #333; color: #00ff00; border: 1px solid #00ff00; }}
            button {{ padding: 8px 16px; background: #00ff00; color: #000; border: none; cursor: pointer; }}
            .request {{ background: #2d2d2d; padding: 15px; margin: 10px 0; border-left: 3px solid #00ff00; }}
            .timestamp {{ color: #888; font-size: 0.9em; }}
            .ip {{ color: #ffff00; }}
            .method {{ color: #ff6666; font-weight: bold; }}
            .path {{ color: #66ccff; }}
            .json {{ background: #1e1e1e; padding: 10px; overflow-x: auto; font-size: 0.85em; }}
            .stats {{ background: #333; padding: 15px; margin-bottom: 20px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚨 OAST Dashboard - Security Testing Logs</h1>
            <p>Real-time logging for SSRF, Callback, Webhook testing</p>
        </div>

        <div class="stats">
            <strong>Total Requests Logged:</strong> {len(requests_list)}<br>
            <strong>Last Request:</strong> {requests_list[0]['timestamp'] if requests_list else 'None'}
        </div>

        <div class="filters">
            <form method="get">
                <input type="text" name="ip" placeholder="Filter by IP" value="{filter_ip}">
                <input type="text" name="method" placeholder="Filter by method (GET, POST, etc)" value="{filter_method}">
                <input type="text" name="search" placeholder="Search in request" value="{search_query}">
                <button type="submit">Filter</button>
                <a href="/oast-dashboard/"><button type="button">Clear</button></a>
            </form>
        </div>

        <h2>Recent Requests:</h2>

        {requests_html}

    </body>
    </html>
    '''

    return HttpResponse(html, content_type='text/html')
