from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from authapp.forms import ShopUserLoginFrom, ShopUserRegisterFrom, ShopUserEditFrom, ShopUserProfileEditForm

# Create your views here.
from django.conf import settings

from authapp.models import ShopUser
from authapp.services import send_verify_email


def login(request):
    title = 'вход'

    next_param = request.GET.get('next', '')

    login_form = ShopUserLoginFrom(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('index'))

    context = {
        'title': title,
        'login_form': login_form,
        'next_param': next_param,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'регистрация'
    if request.method == 'POST':
        register_form = ShopUserRegisterFrom(request.POST, request.FILES)

        if register_form.is_valid():
            new_user = register_form.save()
            send_verify_email(new_user)
            return HttpResponseRedirect(reverse('index'))

    else:
        register_form = ShopUserRegisterFrom()
    context = {
        'title': title,
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)


def edit(request):
    title = 'Редактирование'
    if request.method == 'POST':

        edit_form = ShopUserEditFrom(request.POST, request.FILES, instance=request.user)
        edit_profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)

        if edit_form.is_valid() and edit_profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))

    else:
        edit_form = ShopUserEditFrom(instance=request.user)
        edit_profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    context = {
        'title': title,
        'edit_form': edit_form,
        'edit_profile_form': edit_profile_form,
    }
    return render(request, 'authapp/edit.html', context)


def verify(request, email, key):
    user = ShopUser.objects.filter(email=email).first()
    if user:
        if user.activate_key == key and not user.is_activate_key_expired():
            user.activate_user()
            auth.login(request, user)
    return render(request, 'authapp/register_result.html')
