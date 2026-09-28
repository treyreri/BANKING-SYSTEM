from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Account, Card

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("phone_number" , "password1" , "password2")

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("first_name" , "last_name" , "address" , "passport_id")

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ("card_number" , "cvv" , "date", "type" , "pin")



class TransferForm(forms.Form):
    source_type = forms.ChoiceField( choices=[  ("account", "Account"), ("card", "Card"), ])

    destination_type = forms.ChoiceField(
        choices=[ ("phone", "Phone number"),  ("card", "Card number"), ] )

    receiver_phone = forms.CharField( max_length=20, required=False )
    card_number = forms.CharField( max_length=16, required=False)
    amount = forms.DecimalField( max_digits=12, decimal_places=2, min_value=0.01)

class CheckPhoneForm(forms.Form):
    phone_number = forms.CharField(max_length=20)

class CheckCardForm(forms.Form):
    card_number = forms.CharField(max_length=16)

