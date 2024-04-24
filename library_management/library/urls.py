from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Librarian URLs
    path('librarian/', views.librarian_dashboard, name='librarian_dashboard'),
    path('librarian/documents/', views.manage_documents, name='manage_documents'),
    path('librarian/clients/register/', views.register_client, name='register_client'),
    path('librarian/clients/<str:client_email>/update/', views.update_client, name='update_client'),
    path('librarian/clients/<str:client_email>/delete/', views.delete_client, name='delete_client'),

    # Client URLs
    path('client/', views.client_dashboard, name='client_dashboard'),
    path('client/search/', views.search_documents, name='search_documents'),
    path('client/documents/<int:document_id>/borrow/', views.borrow_document, name='borrow_document'),
    path('client/borrows/<int:borrow_id>/return/', views.return_document, name='return_document'),
    path('client/overdue-fees/', views.pay_overdue_fees, name='pay_overdue_fees'),
    path('client/payment-methods/', views.manage_payment_methods, name='manage_payment_methods'),
]