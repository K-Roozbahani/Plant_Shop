from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .models import User


class AuthenticationForm(forms.Form):
    message = "لطفا شماره مبایل صحیح وارد کنید. شماره مبایل را با صفر وارد کنید. نمونه: 09123456789"

    username = forms.CharField(max_length=16,
                               validators=[RegexValidator(regex=r'^09\d{9}$', message=message)],
                               widget=forms.TextInput(attrs={"placeholder": "شماره مبایل\t 09123456789 "}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": "رمز عبور"}),
    )
    error_messages = {
        "invalid_login": _(
            "لطفا نام کاربری و رمز عبور را به صورت صحیح وارد کنید. نکته: کیبور روی زبان انگلسی باشد"
            " و پسورد به حروف بزرگ و کوچک حساس می باشد."
        ),
        "inactive": _("این کابری غیر فعال می باشد."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        if self.request is None:
            super().__init__(*args, **kwargs)

        else:
            super().__init__(data=request.POST, *args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):

        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"username": _("phone number")},
        )
