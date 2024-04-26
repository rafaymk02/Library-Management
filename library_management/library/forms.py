from django import forms
from .models import Document, Client, OverdueFee, CreditCard, Address
from .models import Document, Book, Magazine, JournalArticle, Author, Publisher


class ClientForm(forms.ModelForm):
    address = forms.CharField(max_length=200)
    card_number = forms.CharField(max_length=20)
    expiration_date = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'placeholder': 'MM/YYYY'}))

    class Meta:
        model = Client
        fields = ['email', 'name', 'password', 'address', 'card_number', 'expiration_date']

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

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'isbn', 'publisher', 'year', 'is_electronic']

class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())
    edition = forms.CharField(max_length=20)

    class Meta:
        model = Book
        fields = ['authors', 'edition', 'pages']

class MagazineForm(forms.ModelForm):
    class Meta:
        model = Magazine
        fields = ['month']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.update(DocumentForm().fields)

class JournalArticleForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all())

    class Meta:
        model = JournalArticle
        fields = ['journal_name', 'authors', 'issue', 'issue_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.update(DocumentForm().fields)

class ElectronicDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'isbn', 'publisher', 'year']