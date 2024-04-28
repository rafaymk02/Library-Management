from django import forms
from .models import Document, Client, OverdueFee, CreditCard, Address, Copy
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
    available_copies = forms.IntegerField(required=False, label="Available Copies")

    class Meta:
        model = Document
        fields = ['title', 'publisher', 'year', 'available_copies']

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        document_instance = kwargs.get('instance')
        if document_instance:
            # Set initial value for available copies
            self.fields['available_copies'].initial = Copy.objects.filter(document=document_instance, available=True).count()


class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(), required=False)
    edition = forms.CharField(max_length=20, required=False)
    pages = forms.IntegerField(required=False)

    class Meta:
        model = Book
        fields = ['authors', 'edition', 'pages']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        document_instance = self.instance.document if self.instance and hasattr(self.instance, 'document') else None
        if document_instance:
            document_form = DocumentForm(instance=document_instance)
            for field_name, field in document_form.fields.items():
                self.fields[field_name] = field


    def save(self, commit=True):
        instance = super().save(commit=False)
        document_instance = instance.document

        if commit:
            document_form = DocumentForm(self.cleaned_data, instance=document_instance)
            if document_form.is_valid():
                document_form.save()  # Save changes to the Document, including available_copies
            instance.save()
            self._save_m2m()  # Save many-to-many data for authors, etc.

            # Update available copies
            current_copies = self.cleaned_data.get('available_copies', 0)
            existing_copies = Copy.objects.filter(document=document_instance, available=True)
            if existing_copies.count() > current_copies:
                # Reduce number of copies if current is less than existing
                existing_copies[current_copies:].update(available=False)
            else:
                # Add new copies if current is more than existing
                for _ in range(current_copies - existing_copies.count()):
                    Copy.objects.create(document=document_instance, available=True)

        return instance



class MagazineForm(forms.ModelForm):
    class Meta:
        model = Magazine
        fields = ['month']

    def __init__(self, *args, **kwargs):
        super(MagazineForm, self).__init__(*args, **kwargs)
        document_instance = self.instance.document if self.instance and hasattr(self.instance, 'document') else None
        if document_instance:
            document_form = DocumentForm(instance=document_instance)
            for field_name, field in document_form.fields.items():
                self.fields[field_name] = field

    def save(self, commit=True):
        instance = super().save(commit=False)
        document_instance = instance.document

        if commit:
            document_form = DocumentForm(self.cleaned_data, instance=document_instance)
            if document_form.is_valid():
                document_form.save()  # Save changes to the Document, including available_copies
            instance.save()
            self._save_m2m()  # Save many-to-many data for authors, etc.

            # Update available copies
            current_copies = self.cleaned_data.get('available_copies', 0)
            existing_copies = Copy.objects.filter(document=document_instance, available=True)
            if existing_copies.count() > current_copies:
                # Reduce number of copies if current is less than existing
                existing_copies[current_copies:].update(available=False)
            else:
                # Add new copies if current is more than existing
                for _ in range(current_copies - existing_copies.count()):
                    Copy.objects.create(document=document_instance, available=True)

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
        document_instance = self.instance.document if self.instance and hasattr(self.instance, 'document') else None
        if document_instance:
            document_form = DocumentForm(instance=document_instance)
            for field_name, field in document_form.fields.items():
                self.fields[field_name] = field

    def save(self, commit=True):
        instance = super().save(commit=False)
        document_instance = instance.document

        if commit:
            document_form = DocumentForm(self.cleaned_data, instance=document_instance)
            if document_form.is_valid():
                document_form.save()  # Save changes to the Document, including available_copies
            instance.save()
            self._save_m2m()  # Save many-to-many data for authors, etc.

            # Update available copies
            current_copies = self.cleaned_data.get('available_copies', 0)
            existing_copies = Copy.objects.filter(document=document_instance, available=True)
            if existing_copies.count() > current_copies:
                # Reduce number of copies if current is less than existing
                existing_copies[current_copies:].update(available=False)
            else:
                # Add new copies if current is more than existing
                for _ in range(current_copies - existing_copies.count()):
                    Copy.objects.create(document=document_instance, available=True)

        return instance



class ElectronicDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'publisher', 'year']