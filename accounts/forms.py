from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, CharField, TextInput

# This is the form the user will have to fill out, when signing up
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','email',)  

# Form to change password 
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = UserChangeForm.Meta.fields  

# Form to update users 'profile'
class UserUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email','first_name', 'last_name', 'role']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['role'].widget.attrs['disabled'] = True 
