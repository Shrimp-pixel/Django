from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from authapp.forms import ShopUserRegisterFrom
from authapp.models import ShopUser
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm
from mainapp.models import ProductCategory, Product

# Create your views here.
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterFrom(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))
    else:
        user_form = ShopUserRegisterFrom()
    context = {
        'form': user_form,
    }
    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    context = {
        'object_list': ShopUser.objects.all().order_by('-is_active')

    }
    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))
    else:
        user_form = ShopUserAdminEditForm(instance=current_user)
    context = {
        'form': user_form,
    }
    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == "POST":
        if current_user.is_active:
            current_user.is_active = False
        else:
            current_user.is_active = True
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:user_list'))

    context = {
        'object': current_user
    }
    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_list'))
    else:
        category_form = ProductCategoryEditForm()
    context = {
        'form': category_form,
    }
    return render(request, 'adminapp/category_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'object_list': ProductCategory.objects.all().order_by('-is_active')

    }
    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    current_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, instance=current_category)

        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_list'))
    else:
        category_form = ProductCategoryEditForm(instance=current_category)
    context = {
        'form': category_form,
    }
    return render(request, 'adminapp/category_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request,pk):
    current_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == "POST":
        if current_category.is_active:
            current_category.is_active = False
        else:
            current_category.is_active = True
        current_category.save()
        return HttpResponseRedirect(reverse('adminapp:category_list'))

    context = {
        'object': current_category
    }
    return render(request, 'adminapp/category_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    context = {

    }
    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    context = {
        'category': get_object_or_404(ProductCategory, pk=pk),
        'object_list': Product.objects.filter(category__pk=pk).order_by('-is_active'),

    }
    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request):
    context = {

    }
    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request):
    context = {

    }
    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def product_detail(request):
    context = {

    }
    return render(request, '', context)
