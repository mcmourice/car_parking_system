# Generated by Django 4.0.4 on 2022-11-18 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0006_rename_email_customer_email_add'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='parking_space',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
