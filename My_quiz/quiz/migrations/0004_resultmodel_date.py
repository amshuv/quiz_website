# Generated by Django 4.2.5 on 2023-11-10 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_alter_resultmodel_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultmodel',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
