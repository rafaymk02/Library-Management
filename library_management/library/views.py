from django.shortcuts import render, redirect
from .models import Document, Client, Librarian, Borrow, OverdueFee, CreditCard
from .forms import DocumentForm, ClientForm, SearchForm, BorrowForm, OverdueFeeForm, CreditCardForm
from django.contrib.auth.decorators import login_required

def librarian_dashboard(request):
    # Render the librarian dashboard template
    return render(request, 'library/librarian_dashboard.html')

def home(request):
    return render(request, 'library/home.html')

def manage_documents(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_documents')
    else:
        form = DocumentForm()
        documents = Document.objects.all()
    return render(request, 'library/manage_documents.html', {'form': form, 'documents': documents})

def register_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('librarian_dashboard')
    else:
        form = ClientForm()
    return render(request, 'library/register_client.html', {'form': form})

def update_client(request):
    if request.method == 'POST':
        client_email = request.POST.get('client_email')
        client = Client.objects.get(email=client_email)
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('librarian_dashboard')
    else:
        clients = Client.objects.all()
        form = ClientForm()
        return render(request, 'library/update_client.html', {'clients': clients, 'form': form})

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
    # Render the client dashboard template
    return render(request, 'library/client_dashboard.html')

def search_documents(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # Perform the search based on the form data
            # Render the search results template with the matching documents
            pass
    else:
        form = SearchForm()
    return render(request, 'library/search_documents.html', {'form': form})

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

@login_required
def manage_payment_methods(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            credit_card = form.save(commit=False)
            credit_card.client = request.user.client
            credit_card.save()
            return redirect('manage_payment_methods')
    else:
        form = CreditCardForm()
        payment_methods = CreditCard.objects.filter(client=request.user.client)
    return render(request, 'library/manage_payment_methods.html', {'form': form, 'payment_methods': payment_methods})