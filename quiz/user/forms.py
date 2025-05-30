from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):

    username = forms.CharField(
        label='Логин', 
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    password = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )



class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль', 
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    password2 = forms.CharField(
        label='Повторите пароль', 
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'})
        }
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        else:
            return cd['password1']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            if get_user_model().objects.filter(email=email).exists():
                raise forms.ValidationError('Пользователь с такой почтой уже существует')
        return email


class UploadImageForm(forms.Form):
    
    photo = forms.ImageField(label='')



