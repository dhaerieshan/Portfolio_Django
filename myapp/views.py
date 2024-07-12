from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

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
