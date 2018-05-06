from django import forms
from django.core.validators import RegexValidator
from .models import USERNAME_VALIDATE, PasswordForget
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import Q
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _


User = get_user_model()
# admin form


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_admin', 'is_staff',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


# User Login form
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150,label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_obj = User.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=username)
        ).distinct()
        if not user_obj.exists() and user_obj.count() != 1:
            raise forms.ValidationError('Invalid Information')
        user_obj = user_obj.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError('Invalid Information')
        if not user_obj.is_active:
            raise forms.ValidationError('Inactive user')
        self.cleaned_data['user'] = user_obj
        return super(UserLoginForm, self).clean()


# User create form
class UserCreateForm(forms.ModelForm):
    password = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Password')
    username = forms.CharField(validators=[RegexValidator(
        regex=USERNAME_VALIDATE,
        message='Invalid Username',
        code='Invalid Username'

    )])

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': _('Username'),
            'email': _('Email')
        }
        help_texts = {
            'username': _('content alpha-numeric and "._"')
        }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


# User Forget Password
class PasswordForgetForm(forms.ModelForm):
    user = forms.CharField(max_length=100)

    class Meta:
        model = PasswordForget
        fields = ['user']
        labels = {'user': _('Username')}

    def clean_user(self):
        user = self.cleaned_data.get('user')
        user_obj = User.objects.filter(username__iexact=user)
        if not user_obj.exists():
            raise forms.ValidationError('User Does not exist')
        self.cleaned_data['user'] = user_obj.first()
        return user_obj.first()


# Reset Forget Password
class ResetPasswordForm(forms.Form):
    password = forms.CharField(max_length=150, widget=forms.PasswordInput(), label='New Password')
    retype_password = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Retype Password')

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('retype_password')
        if not password == confirm_password:
            raise forms.ValidationError('Password Does not match')
        return super(ResetPasswordForm, self).clean()


# Change Password
class ForgetPasswordForm(forms.Form):
    current_password = forms.CharField(max_length=150, widget=forms.PasswordInput(), label='Current Password')
    new_password = forms.CharField(max_length=150, widget=forms.PasswordInput(), label='New Password')
    retype_password = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Retype Password')

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        retype_password = self.cleaned_data.get('retype_password')
        if not new_password == retype_password:
            raise forms.ValidationError('Password Does not match')
        return super(ForgetPasswordForm, self).clean()

