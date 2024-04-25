from django.shortcuts import render, redirect
from .models import Document, Client, Librarian, Borrow, OverdueFee, CreditCard
from .forms import DocumentForm, ClientForm, SearchForm, BorrowForm, OverdueFeeForm, CreditCardForm
from django.contrib.auth.decorators import login_required

def librarian_dashboard(request):
    librarian_id = request.session.get('librarian_id')
    if librarian_id:
        librarian = Librarian.objects.get(ssn=librarian_id)
        return render(request, 'library/librarian_dashboard.html', {'librarian': librarian})
    else:
        return redirect('librarian_login')

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