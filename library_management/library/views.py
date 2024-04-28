from django.shortcuts import render, redirect
from .models import Document, Client, Librarian, Borrow, OverdueFee, CreditCard, Address, Publisher, Copy
from .forms import DocumentForm, ClientForm, SearchForm, BorrowForm, OverdueFeeForm, CreditCardForm, BookForm, MagazineForm, JournalArticleForm, ElectronicDocumentForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)


def librarian_dashboard(request):
    librarian_id = request.session.get('librarian_id')
    if librarian_id:
        librarian = Librarian.objects.get(ssn=librarian_id)
        return render(request, 'library/librarian_dashboard.html', {'librarian': librarian})
    else:
        return redirect('librarian_login')

def home(request):
    return render(request, 'library/home.html')

def borrow_document(request, document_id):
    document = Document.objects.get(id=document_id)
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            # Process the borrowing of the document
            # Render a success message or redirect to the client dashboard
            pass
    else:
        form = BorrowForm()
    return render(request, 'library/borrow_document.html', {'form': form, 'document': document})

def return_document(request, borrow_id):
    borrow = Borrow.objects.get(id=borrow_id)
    # Process the return of the document
    # Calculate overdue fees if applicable
    # Render a success message or redirect to the client dashboard
    pass

def register_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()

            address = Address(client=client, address=form.cleaned_data['address'])
            address.save()

            expiration_date_str = form.cleaned_data['expiration_date']
            expiration_date = datetime.strptime(expiration_date_str, '%m/%Y').date()

            credit_card = CreditCard(client=client, card_number=form.cleaned_data['card_number'],
                                     expiration_date=expiration_date, payment_address=address)
            credit_card.save()

            return redirect('librarian_dashboard')
    else:
        form = ClientForm()
    return render(request, 'library/register_client.html', {'form': form})

def update_client(request):
    if request.method == 'POST':
        client_email = request.POST.get('client_email')
        client = Client.objects.get(email=client_email)

        if 'delete_address' in request.POST:
            address_id = request.POST.get('delete_address')
            address = Address.objects.get(id=address_id)
            address.delete()
        elif 'add_address' in request.POST:
            new_address = request.POST.get('new_address')
            Address.objects.create(client=client, address=new_address)
        elif 'delete_credit_card' in request.POST:
            credit_card_id = request.POST.get('delete_credit_card')
            credit_card = CreditCard.objects.get(id=credit_card_id)
            credit_card.delete()
        elif 'add_credit_card' in request.POST:
            new_card_number = request.POST.get('new_card_number')
            new_expiration_date = request.POST.get('new_expiration_date')

            expiration_date = datetime.strptime(new_expiration_date, '%Y-%m').date()

            # Get the client's first address as the payment address
            payment_address = client.address_set.first()

            CreditCard.objects.create(client=client, card_number=new_card_number, expiration_date=expiration_date, payment_address=payment_address)
        else:
            client.name = request.POST.get('name')
            client.email = request.POST.get('email')
            client.password = request.POST.get('password')
            client.save()

        return redirect('librarian_dashboard')
    else:
        clients = Client.objects.all()
        return render(request, 'library/update_client.html', {'clients': clients})

def delete_client(request):
    if request.method == 'POST':
        client_email = request.POST.get('client_email')
        client = Client.objects.get(email=client_email)
        client.delete()
        return redirect('librarian_dashboard')
    else:
        clients = Client.objects.all()
        return render(request, 'library/delete_client.html', {'clients': clients})

def client_dashboard(request):
    client_email = request.session.get('client_email')
    if client_email:
        client = Client.objects.get(email=client_email)
        return render(request, 'library/client_dashboard.html', {'client': client})
    else:
        return redirect('client_login')

def client_logout(request):
    del request.session['client_email']
    return redirect('client_login')

def search_documents(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            title_search_type = form.cleaned_data.get('title_search_type')
            publisher_name = form.cleaned_data.get('publisher_name')
            publisher_search_type = form.cleaned_data.get('publisher_search_type')
            year = form.cleaned_data.get('year')
            search_logic = form.cleaned_data.get('search_logic')

            queries = []
            if title:
                if title_search_type == 'contains':
                    queries.append(Q(title__icontains=title))
                elif title_search_type == 'exact':
                    queries.append(Q(title__iexact=title))
                elif title_search_type == 'startswith':
                    queries.append(Q(title__istartswith=title))

            if publisher_name:
                if publisher_search_type == 'contains':
                    queries.append(Q(publisher__name__icontains=publisher_name))
                elif publisher_search_type == 'exact':
                    queries.append(Q(publisher__name__iexact=publisher_name))
                elif publisher_search_type == 'startswith':
                    queries.append(Q(publisher__name__istartswith=publisher_name))

            if year:
                queries.append(Q(year=year))

            final_query = queries.pop(0) if queries else Q()
            for query in queries:
                if search_logic == 'AND':
                    final_query &= query
                else:
                    final_query |= query

            # Annotate each document with the count of available copies
            documents = Document.objects.filter(final_query).annotate(
                available_copies=Count('copy', filter=Q(copy__available=True))
            ).filter(available_copies__gt=0)

            return render(request, 'library/search_documents.html', {'form': form, 'documents': documents})
    else:
        form = SearchForm()

    return render(request, 'library/search_documents.html', {'form': form})

def pay_overdue_fees(request):
    if request.method == 'POST':
        form = OverdueFeeForm(request.POST)
        if form.is_valid():
            # Process the payment of overdue fees
            # Render a success message or redirect to the client dashboard
            pass
    else:
        form = OverdueFeeForm()
    return render(request, 'library/pay_overdue_fees.html', {'form': form})

def manage_payment_methods(request):
    client_email = request.session.get('client_email')
    if client_email:
        client = Client.objects.get(email=client_email)
        if request.method == 'POST':
            if 'add_payment_method' in request.POST:
                card_number = request.POST.get('card_number')
                expiration_date_str = request.POST.get('expiration_date')
                payment_address_str = request.POST.get('payment_address')

                # Parse the expiration date in the "YYYY-MM" format
                expiration_date = datetime.strptime(expiration_date_str, '%Y-%m').date()

                payment_address = Address.objects.create(client=client, address=payment_address_str)

                CreditCard.objects.create(client=client, card_number=card_number, expiration_date=expiration_date, payment_address=payment_address)
            elif 'delete_payment_method' in request.POST:
                credit_card_id = request.POST.get('delete_payment_method')
                CreditCard.objects.filter(id=credit_card_id, client=client).delete()
            return redirect('manage_payment_methods')
        payment_methods = CreditCard.objects.filter(client=client)
        return render(request, 'library/manage_payment_methods.html', {'payment_methods': payment_methods})
    else:
        return redirect('client_login')

def manage_documents(request):
    if request.method == 'POST':
        document_form = DocumentForm(request.POST)
        logger.debug("Received POST request with data: %s", request.POST)
        if document_form.is_valid():
            document = document_form.save(commit=False)
            document_type = request.POST.get('document_type')
            document.is_electronic = request.POST.get('is_electronic', 'off') == 'on'
            document.save()

            if document_type == 'Book':
                book_form = BookForm(request.POST)
                if book_form.is_valid():
                    book = book_form.save(commit=False)
                    book.document = document
                    book.save()
                    book_form.save_m2m()
                else:
                    print(book_form.errors)  # Print errors to the console

            elif document_type == 'Magazine':
                magazine_form = MagazineForm(request.POST)
                if magazine_form.is_valid():
                    magazine = magazine_form.save(commit=False)
                    magazine.document = document
                    magazine.save()

            elif document_type == 'JournalArticle':
                journal_article_form = JournalArticleForm(request.POST)
                if journal_article_form.is_valid():
                    journal_article = journal_article_form.save(commit=False)
                    journal_article.document = document
                    journal_article.save()
                    journal_article_form.save_m2m()

            num_copies = int(request.POST.get('num_copies', 1))
            # Assuming Copy is defined correctly elsewhere in your models
            for _ in range(num_copies):
                Copy.objects.create(document=document)

            return redirect('manage_documents')  # Redirect to a safe URL

        else:
            print(document_form.errors)  # Print document form errors

    else:
        document_form = DocumentForm()
        book_form = BookForm()
        magazine_form = MagazineForm()
        journal_article_form = JournalArticleForm()

    documents = Document.objects.annotate(
        available_copies=Count('copy', filter=Q(copy__available=True))
    )

    context = {
        'document_form': document_form,
        'book_form': book_form,
        'magazine_form': magazine_form,
        'journal_article_form': journal_article_form,
        'documents': documents,
    }
    return render(request, 'library/manage_documents.html', context)


def librarian_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            librarian = Librarian.objects.get(email=email)
            if librarian.password == password:
                request.session['librarian_id'] = librarian.ssn
                return redirect('librarian_dashboard')
            else:
                error_message = 'Invalid password'
        except Librarian.DoesNotExist:
            error_message = 'Librarian does not exist'
        return render(request, 'library/librarian_login.html', {'error_message': error_message})
    return render(request, 'library/librarian_login.html')

def librarian_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        ssn = request.POST.get('ssn')
        email = request.POST.get('email')
        password = request.POST.get('password')
        salary = request.POST.get('salary')
        librarian = Librarian(ssn=ssn, name=name, email=email, password=password, salary=salary)
        librarian.save()
        request.session['librarian_id'] = librarian.ssn
        return redirect('librarian_dashboard')
    return render(request, 'library/librarian_register.html')

def librarian_logout(request):
    del request.session['librarian_id']
    return redirect('librarian_login')

def client_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            client = Client.objects.get(email=email)
            if client.password == password:
                request.session['client_email'] = client.email
                return redirect('client_dashboard')
            else:
                error_message = 'Invalid password'
        except Client.DoesNotExist:
            error_message = 'Client does not exist'
        return render(request, 'library/client_login.html', {'error_message': error_message})
    return render(request, 'library/client_login.html')

def update_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    # Determine the type and select the correct form
    if hasattr(document, 'book'):
        document_specific_instance = document.book
        DocumentSpecificForm = BookForm
    elif hasattr(document, 'magazine'):
        document_specific_instance = document.magazine
        DocumentSpecificForm = MagazineForm
    elif hasattr(document, 'journalarticle'):
        document_specific_instance = document.journalarticle
        DocumentSpecificForm = JournalArticleForm
    else:
        document_specific_instance = document
        DocumentSpecificForm = DocumentForm

    if request.method == 'POST':
        form = DocumentSpecificForm(request.POST, instance=document_specific_instance)
        if form.is_valid():
            form.save()
            return redirect('manage_documents')
    else:
        form = DocumentSpecificForm(instance=document_specific_instance)

    return render(request, 'library/update_document.html', {'form': form})
