from django.db import models

class Librarian(models.Model):
    ssn = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

class Client(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)

class CreditCard(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20)
    expiration_date = models.DateField()
    payment_address = models.ForeignKey(Address, on_delete=models.CASCADE)

class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=[
        ('Book', 'Book'),
        ('Magazine', 'Magazine'),
        ('JournalArticle', 'Journal Article')
    ])
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    year = models.IntegerField()
    is_electronic = models.BooleanField(default=False)

class Book(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, primary_key=True)
    authors = models.ManyToManyField(Author)
    edition = models.CharField(max_length=20)
    pages = models.IntegerField()

class Magazine(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, primary_key=True)
    month = models.CharField(max_length=20)

class JournalArticle(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, primary_key=True)
    journal_name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    issue = models.IntegerField()
    issue_number = models.IntegerField()

class Copy(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

class Borrow(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    copy = models.ForeignKey(Copy, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

class OverdueFee(models.Model):
    id = models.AutoField(primary_key=True)
    borrow = models.ForeignKey(Borrow, on_delete=models.CASCADE)
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)