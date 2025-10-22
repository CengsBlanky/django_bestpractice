from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    UserChangeForm,
)
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

# Register your models here.


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="密码", widget=forms.PasswordInput)
    password2 = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("username", "phone", "gender")

    def clean_phone(self):
        return self.cleaned_data.get("phone")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码输入不一致，请确认")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.phone = self.cleaned_data["phone"]
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField()

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.phone = self.cleaned_data["phone"]
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ("username", "phone", "gender")
    search_fields = ("username", "phone", "gender")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "phone",
                    "gender",
                    "password",
                )
            },
        ),
        (
            _("Permissions"),
            {"fields": ("is_staff", "is_superuser", "user_permissions")},
        ),
        (
            _("Date Info"),
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "phone",
                    "date_joined",
                    "gender",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("username", "phone", "gender")


admin.site.register(CustomUser, CustomUserAdmin)
