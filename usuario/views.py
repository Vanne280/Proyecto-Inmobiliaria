from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import SignupForm
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

#envio de correo para activar cuenta
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

#ListView
from django.views.generic.list import ListView

#Decorador (permisos)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

# Registro de usuarios
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            SendEmailActivateUser(request, user)
            logout(request)
            return HttpResponseRedirect(reverse("usuario:emailsent", args=[user.username]))
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

#Enviar correo electrónico para activar Usuario
def SendEmailActivateUser(request, user):
    current_site = get_current_site(request)
    subject = 'Activar cuenta inmobiliaria'
    html_content = render_to_string('email/account_activation.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
            subject, text_content, from_email=settings.EMAIL_HOST_USER, to=[user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

#Activar un usuario que previamente se ha registrado
def ActivateUser(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = 1
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')
    else:
        return render(request, 'registration/account_activation_invalid.html')

#Renderiza el template account_activation.html
def templateEmailSent(request, username):
    return render(request, 'registration/account_activation.html', {'username': username})

# class UserList(PermissionRequiredMixin, ListView):
#     permission_required = 'users.listarusuarios'
#     model = User
#
# @login_required
# def UserApp(request):
#     return render(request, "auth/user_app.html")
