from django import forms
from .models import Document, Client, OverdueFee, CreditCard, Address

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'name', 'password']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address']

class CreditCardForm(forms.ModelForm):
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'month'}))
    payment_address = forms.ModelChoiceField(queryset=Address.objects.none())

    class Meta:
        model = CreditCard
        fields = ['card_number', 'expiration_date', 'payment_address']

    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        super().__init__(*args, **kwargs)
        if client:
            self.fields['payment_address'].queryset = client.address_set.all()

class SearchForm(forms.Form):
    pass

class BorrowForm(forms.Form):
    pass

class OverdueFeeForm(forms.ModelForm):
    class Meta:
        model = OverdueFee
        fields = '__all__'

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = '__all__'