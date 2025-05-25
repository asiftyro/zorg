"""account/forms.py"""

from django.conf import settings
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from altcha import verify_solution
from .models import Account


class AccountCreateForm(forms.ModelForm):
    """Account create form"""

    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        """Meta of AccountCreateForm"""

        model = Account
        fields = (
            "username",
            "is_active",
            "full_name",
            "email",
            "phone",
            "designation",
            "password",
            "password2",
            "groups",
        )

    def clean_password2(self):
        """Clean password"""
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            self.save_m2m()  # Save many-to-many relationships (groups)
        return user


class AccountUpdateForm(forms.ModelForm):
    """Account update form"""

    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank to keep existing password",
    )
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        """Meta of AccountUpdateForm"""

        model = Account
        fields = (
            "username",
            "is_active",
            "full_name",
            "email",
            "phone",
            "designation",
            "password",
            "password2",
            "groups",
        )

    def clean_password2(self):
        """Clean password"""
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)

        # Update password only if provided
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
            self.save_m2m()  # Save groups
        return user


class AccountLoginForm(AuthenticationForm):
    """Account login form"""

    altcha = forms.CharField()

    def clean(self):
        altcha = self.cleaned_data.get("altcha")
        if not altcha:
            raise forms.ValidationError("Altcha is required.")

        try:
            verified, err = verify_solution(altcha, settings.ALTCHA_HMAC_KEY, True)
            if not verified:
                raise forms.ValidationError(f"Invalid Altcha solution. Error: {err}")
        except Exception as err:
            raise forms.ValidationError(f"Altcha validation failed: {err}")

        super().clean()
        return self.cleaned_data


class AccountSelfUpdateForm(forms.ModelForm):
    """Account self update form"""

    password = forms.CharField(
        widget=forms.PasswordInput,
        strip=False,
        required=False,
        help_text="Leave blank to keep existing password",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank to keep existing password",
    )

    class Meta:
        """Meta of AppUserSelfEditForm"""

        model = Account
        fields = (
            "full_name",
            "email",
            "phone",
            "password",
            "password2",
        )

    def clean_password2(self):
        """Clean password"""
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)

        # Update password only if provided
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
            self.save_m2m()  # Save groups
        return user
