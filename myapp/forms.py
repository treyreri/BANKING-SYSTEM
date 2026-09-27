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
    receiver_phone = forms.CharField(max_length=20)
    amount = forms.DecimalField(max_digits=12, decimal_places=2)
    source_type = forms.ChoiceField(
        choices = [ ("account" , "Account") , ("card" , "Card") ] )
    card_number = forms.CharField(required = False)

class CheckPhoneForm(forms.Form):
    phone_number = forms.CharField(max_length=20)

class CheckCardForm(forms.Form):
    card_number = forms.CharField(max_length=16)

