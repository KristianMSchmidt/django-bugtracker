from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm


# This is the form the user will have to fill out, when signing up
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','email',)

# Form to change password 
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields  # __all__   by defailr


# Form to update users 'profile'
class UserUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
