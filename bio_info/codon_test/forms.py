from django import forms
from Bio.Seq import Seq
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()

class UploadCodonForm(forms.Form):
    form = forms.CharField()

    def clean_form(self):
        form = Seq(self.cleaned_data['form'].upper())
        if len(form) != 3:
            raise ValueError("некорректрый кодон - должен содержать 3 элемента!")
        for i in form.strip():
            if i not in ('A', 'C', 'G', 'T'):
                raise ValueError("некорректрый кодон - должен содержать: 'A', 'C', 'G', 'T'!")
        return form


class UserLoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            qs = User.objects.filter(username=username)
            if not qs.exists():
                raise forms.ValidationError('Пользователь не зарегистрирован!')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Неверный пароль!')
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegForm(forms.ModelForm):
    username = forms.CharField(label="Введите имя пользователя")
    password = forms.CharField(label="Введите пароль", widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
    password2 = forms.CharField(label="Введите пароль еще раз", widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))

    class Meta:
        model = User
        fields = ('username', )

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return data['password2']