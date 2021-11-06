from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    email = forms.CharField(label="Email", required=True)

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if first_name == "" and last_name == "":
            raise ValidationError("First name or Last name is required")
        return cleaned_data

    class Meta(UserCreationForm.Meta):
        fields = ["username", "first_name",
                  "last_name", "email", "password1", "password2"]


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "email"]
        labels = {"first_name": "Name", "email": "Email"}


class PasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(label="Old password", strip=False,
                                   widget=forms.PasswordInput)
    password = forms.CharField(label="Password", strip=False,
                               widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirm password", strip=False,
                                       widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data["password"]
        password_confirm = self.cleaned_data["password_confirm"]
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords are not equal")
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.instance.check_password(old_password):
            raise forms.ValidationError("Wrong old password")
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ["old_password", "password", "password_confirm"]
