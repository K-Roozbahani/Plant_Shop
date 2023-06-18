from django import forms
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .models import User


# from django.contrib.auth.forms import UserCreationForm

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


class UserRegisterForm(forms.ModelForm):

    message = "لطفا شماره مبایل صحیح وارد کنید. شماره مبایل را با صفر وارد کنید. نمونه: 09123456789"

    error_messages = {
        "password_mismatch": "پسورد اول و دوم همسان نمی باشند",
    }

    phone_number = forms.CharField(max_length=16,
                                   validators=[RegexValidator(regex=r'^09\d{9}$', message=message)],
                                   widget=forms.TextInput(attrs={"placeholder": "شماره مبایل\t 09123456789 "}))
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"placeholder": "نام"}), )
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"placeholder": "نام خانوادگی"}), )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "رمز عبور"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "تکرار رمز عبور"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("phone_number", "first_name", "last_name")

    def __init__(self, request=None, *args, **kwargs):
        if request is not None:
            kwargs["data"] = request.POST
        super().__init__(*args, **kwargs)
        self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
            "autofocus"
        ] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
