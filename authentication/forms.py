from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.CharField(
        max_length=30, label="",
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
        required=True,
    )
    first_name = forms.CharField(
        max_length=50,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
        required=True,
    )
    last_name = forms.CharField(
        max_length=50,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
        required=True,
    )
    password1 = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        label="",
        required=True,
    )
    password2 = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
        label="",
        required=True,
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        label="",
    )
    mobile = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Mobile Number'}),
        label="",
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder": "Birth Date: yyyy-MM-dd"}),
        label="",
        required=True,
    )

    class Meta:
        # get_user_model() instead of models.User when User-model is modified
        model = get_user_model()
        fields = ["email", "first_name", "last_name", "password1", "password2",
                  "phone", "mobile", "birth_date"]
