from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class RegisterForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput({
        'class': 'white-text center-align'
    }))

    email = forms.EmailField(widget=forms.EmailInput({
        'class': 'white-text center-align'
    }))

    password = forms.CharField(widget=forms.PasswordInput({
        'class': 'white-text center-align'
    }))

    def clean(self, *args, **kwargs):

        username = self.cleaned_data['username']
        email = self.cleaned_data['email']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username is already taken.')
        elif User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address is already taken.')

        return super(RegisterForm, self).clean(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput({
        'class': 'white-text center-align'
    }))

    password = forms.CharField(widget=forms.PasswordInput({
        'class': 'white-text center-align'
    }))

    def clean(self, *args, **kwargs):

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not username: raise forms.ValidationError('Username is missing.')
        elif not password: raise forms.ValidationError('Password is missing.')

        user = authenticate(username=username, password=password)

        if not user or not user.check_password(password):
            raise forms.ValidationError('Incorrect username or password.')

        return super(LoginForm, self).clean(*args, **kwargs)