from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import auth

class EmailValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            if not validate_email(email):
                return JsonResponse({'email_error': 'Email is invalid'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'email_error': 'Sorry, email is already in use. Please choose another one.'}, status=409)
            return JsonResponse({'email_valid': True})
        except KeyError:
            return JsonResponse({'error': 'Email not provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class UsernameValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data['username']
            if not str(username).isalnum():
                return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({'username_error': 'Sorry, username is already in use. Please choose another one.'}, status=409)
            return JsonResponse({'username_valid': True})
        except KeyError:
            return JsonResponse({'error': 'Username not provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active=False
                user.save()
                messages.success(request, 'Account successfully created')
                return redirect('login')

        return render(request, 'authentication/register.html')
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)  # Log in the user
                return redirect('dashboard')
        
        return redirect('dashboard')  # Redirect to login page if authentication fails

        