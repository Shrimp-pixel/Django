from django.contrib.auth.decorators import user_passes_test
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.db.models import F
from django.db import connection

from authapp.forms import ShopUserRegisterFrom
from authapp.models import ShopUser
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

# Create your views here.
from mainapp.models import ProductCategory, Product


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)


class AccessMixin:

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


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


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#    context = {
#        'object_list': ShopUser.objects.all().order_by('-is_active')
#
#    }
#    return render(request, 'adminapp/users.html', context)

class UserListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    ordering = '-is_active'


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


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#    context = {
#        'object_list': ProductCategory.objects.all().order_by('-is_active')
#
#    }
#    return render(request, 'adminapp/categories.html', context)


class CategoryListView(AccessMixin, ListView):
    model = ProductCategory
    ordering = '-is_active'
    template_name = 'adminapp/categories.html'


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#    current_category = get_object_or_404(ProductCategory, pk=pk)
#    if request.method == 'POST':
#        category_form = ProductCategoryEditForm(request.POST, instance=current_category)

#        if category_form.is_valid():
#            category_form.save()
#            return HttpResponseRedirect(reverse('adminapp:category_list'))
#    else:
#        category_form = ProductCategoryEditForm(instance=current_category)
#    context = {
#        'form': category_form,
#    }
#    return render(request, 'adminapp/category_form.html', context)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    form_class = ProductCategoryEditForm
    template_name = 'adminapp/product_form.html'
    success_url = reverse_lazy('adminapp:category_list')

    def get_success_url(self):
        return reverse('adminapp:category_update', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data.get('discount')
            if discount:
                self.object.product_set.update(
                    price=F('price') * (1 - discount / 100.0)
                )
        return super().form_valid(form)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
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


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request):
#    context = {
#
#    }
#    return render(request, '', context)


class ProductCreateView(AccessMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('adminapp:product_list', args=[self.kwargs['pk']])


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#    context = {
#        'category': get_object_or_404(ProductCategory, pk=pk),
#        'object_list': Product.objects.filter(category__pk=pk).order_by('-is_active'),
#
#    }
#    return render(request, 'adminapp/products.html', context)


class ProductsListView(AccessMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context_data

    def get_queryset(self):
        return Product.objects.filter(category__pk=self.kwargs.get('pk'))


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request):
#    context = {
#
#    }
#    return render(request, '', context)

class ProductUpdateView(AccessMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request):
#    context = {
#
#    }
#    return render(request, '', context)

class ProductDelete(AccessMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        product_item = Product.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


# @user_passes_test(lambda u: u.is_superuser)
# def product_detail(request, pk):
#    context = {
#
#    }
#    return render(request, '', context)


class ProductDetailView(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'
