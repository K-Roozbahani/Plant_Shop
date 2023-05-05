from django import forms
from .models import DeliveryInformation


class DeliveryInformationForm(forms.ModelForm):
    class Meta:
        model = DeliveryInformation
        fields = ["first_name", "last_name", "address", "state", "city",
                  "postal_code", "email", "phone_number", "description"]
