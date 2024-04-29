from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Librarian URLs
    path('librarian/', views.librarian_dashboard, name='librarian_dashboard'),
    path('librarian/documents/', views.manage_documents, name='manage_documents'),
    path('librarian/clients/register/', views.register_client, name='register_client'),
    path('librarian/clients/update/', views.update_client, name='update_client'),
    path('librarian/clients/delete/', views.delete_client, name='delete_client'),
    path('librarian/login/', views.librarian_login, name='librarian_login'),
    path('librarian/register/', views.librarian_register, name='librarian_register'),
    path('librarian/logout/', views.librarian_logout, name='librarian_logout'),
    path('librarian/documents/update/<int:document_id>/', views.update_document, name='update_document'),


    # Client URLs
    path('client/', views.client_dashboard, name='client_dashboard'),
    path('client/login/', views.client_login, name='client_login'),
    path('client/logout/', views.client_logout, name='client_logout'),
    path('client/search/', views.search_documents, name='search_documents'),
    path('client/documents/<int:document_id>/borrow/', views.borrow_document, name='borrow_document'),
    path('client/borrows/<int:borrow_id>/return/', views.return_document, name='return_document'),
    path('client/overdue-fees/', views.pay_overdue_fees, name='pay_overdue_fees'),
    path('client/payment-methods/', views.manage_payment_methods, name='manage_payment_methods'),
]