# Generated by Django 5.0.4 on 2024-04-26 20:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0002_librarian_password"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="author",
            name="documents",
        ),
        migrations.RemoveField(
            model_name="document",
            name="available_copies",
        ),
        migrations.AddField(
            model_name="book",
            name="authors",
            field=models.ManyToManyField(to="library.author"),
        ),
        migrations.AddField(
            model_name="document",
            name="is_electronic",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="journalarticle",
            name="authors",
            field=models.ManyToManyField(to="library.author"),
        ),
        migrations.AlterField(
            model_name="document",
            name="type",
            field=models.CharField(
                choices=[
                    ("Book", "Book"),
                    ("Magazine", "Magazine"),
                    ("JournalArticle", "Journal Article"),
                ],
                max_length=20,
            ),
        ),
    ]