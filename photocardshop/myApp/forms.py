from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Card

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
       class Meta:
           model = User
           fields = ['username', 'email', 'first_name', 'last_name']
   
       def __init__(self, *args, **kwargs):
           super(UserUpdateForm, self).__init__(*args, **kwargs)
           for fieldname in ['username', 'email', 'first_name', 'last_name']:
               self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

class AddCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'description', 'rarity', 'price', 'image', 'is_featured']

    def __init__(self, *args, **kwargs):
        super(AddCardForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
   