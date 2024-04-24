from django import forms
from .models import Document, Client, OverdueFee, CreditCard

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

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