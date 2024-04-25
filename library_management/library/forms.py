from django import forms
from .models import Document, Client, OverdueFee, CreditCard, Address

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

class ClientForm(forms.ModelForm):
    address = forms.CharField(max_length=200)
    card_number = forms.CharField(max_length=20)
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Client
        fields = ['email', 'name', 'password', 'address', 'card_number', 'expiration_date']

class SearchForm(forms.Form):
    # Add search form fields based on your requirements
    pass

class BorrowForm(forms.Form):
    # Add borrow form fields based on your requirements
    pass

class OverdueFeeForm(forms.ModelForm):
    class Meta:
        model = OverdueFee
        fields = '__all__'

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = '__all__'