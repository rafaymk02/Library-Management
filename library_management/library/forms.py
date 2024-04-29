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
    title = forms.CharField(required=False, label="Title")
    title_search_type = forms.ChoiceField(choices=[('contains', 'Contains'), ('exact', 'Exact'), ('startswith', 'Starts With')], required=False, label="Title Search Type")
    publisher_name = forms.CharField(required=False, label="Publisher Name")
    publisher_search_type = forms.ChoiceField(choices=[('contains', 'Contains'), ('exact', 'Exact'), ('startswith', 'Starts With')], required=False, label="Publisher Search Type")
    year = forms.IntegerField(required=False, label="Year")
    search_logic = forms.ChoiceField(choices=[('AND', 'AND'), ('OR', 'OR')], initial='AND', label="Search Logic")

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
        fields = ['title', 'publisher', 'year']

class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(), required=False)
    edition = forms.CharField(max_length=20, required=False)
    pages = forms.IntegerField(required=False)

    class Meta:
        model = Book
        fields = ['authors', 'edition', 'pages']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        document_instance = self.instance.document if self.instance and hasattr(self.instance, 'document') else Document()
        document_fields = DocumentForm(instance=document_instance).fields
        self.fields.update(document_fields)

    def save(self, commit=True):
        instance = super().save(commit=False)
        document_instance = getattr(instance, 'document', None)
        if document_instance:
            # Update the existing document instance
            DocumentForm(self.cleaned_data, instance=document_instance).save()
        else:
            # Create a new document instance
            document_instance = DocumentForm(self.cleaned_data).save()
        instance.document = document_instance

        if commit:
            instance.save()
        return instance


class MagazineForm(forms.ModelForm):
    class Meta:
        model = Magazine
        fields = ['month']

    def __init__(self, *args, **kwargs):
        super(MagazineForm, self).__init__(*args, **kwargs)
        document_instance = self.instance.document if self.instance and hasattr(self.instance, 'document') else Document()
        document_fields = DocumentForm(instance=document_instance).fields
        self.fields.update(document_fields)

    def save(self, commit=True):
        instance = super().save(commit=False)
        document_instance = getattr(instance, 'document', None)
        if document_instance:
            # Update the existing document instance
            DocumentForm(self.cleaned_data, instance=document_instance).save()
        else:
            # Create a new document instance
            document_instance = DocumentForm(self.cleaned_data).save()
        instance.document = document_instance

        if commit:
            instance.save()
        return instance



class JournalArticleForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(), required=False)
    journal_name = forms.CharField(max_length=100, required=False)
    issue = forms.IntegerField(required=False)
    issue_number = forms.IntegerField(required=False)

    class Meta:
        model = JournalArticle
        fields = ['journal_name', 'issue', 'issue_number', 'authors']

    def __init__(self, *args, **kwargs):
        super(JournalArticleForm, self).__init__(*args, **kwargs)
        document_instance = self.instance.document if self.instance and hasattr(self.instance, 'document') else Document()
        document_fields = DocumentForm(instance=document_instance).fields
        self.fields.update(document_fields)

    def save(self, commit=True):
        instance = super().save(commit=False)
        document_instance = getattr(instance, 'document', None)
        if document_instance:
            # Update the existing document instance
            DocumentForm(self.cleaned_data, instance=document_instance).save()
        else:
            # Create a new document instance
            document_instance = DocumentForm(self.cleaned_data).save()
        instance.document = document_instance

        if commit:
            instance.save()
        return instance


class ElectronicDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'publisher', 'year']