from authapp.forms import ShopUserEditFrom
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.forms import ModelForm


class ShopUserAdminEditForm(ShopUserEditFrom):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryEditForm(ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductEditForm(ModelForm):
    class Meta:
        model = Product
        #fields = '__all__'
        exclude = ('is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
