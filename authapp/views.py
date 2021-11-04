from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from authapp.forms import ShopUserLoginFrom, ShopUserRegisterFrom, ShopUserEditFrom


# Create your views here.
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
            register_form.save()
            return HttpResponseRedirect(reverse('index'))

    else:
        register_form = ShopUserRegisterFrom()
    context = {
        'title': title,
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)


def edit(request):
    title = 'редактирование'
    if request.method == 'POST':

        edit_form = ShopUserEditFrom(request.POST, request.FILES, instance=request.user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))

    else:
        edit_form = ShopUserEditFrom(instance=request.user)
    context = {
        'title': title,
        'edit_form': edit_form
    }
    return render(request, 'authapp/edit.html', context)
