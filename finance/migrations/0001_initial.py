# Generated by Django 2.0.5 on 2018-05-05 10:53

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('account_type', models.IntegerField(choices=[(1, 'Personal'), (2, 'Foreign'), (3, 'System')], default=1)),
                ('active', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('show_on_dashboard', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-active', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('active', models.BooleanField(default=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='ImportConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('headers', models.BooleanField(help_text='First line contains headers')),
                ('dateformat', models.CharField(max_length=32)),
                ('config', models.TextField()),
                ('default_account', models.ForeignKey(blank=True, limit_choices_to={'account_type': 1}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.Account')),
            ],
        ),
        migrations.CreateModel(
            name='ImportFile',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='imports')),
            ],
        ),
        migrations.CreateModel(
            name='RecurringTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('recurrence', models.IntegerField(choices=[(0, 'Disabled'), (1, 'Monthly'), (2, 'Quarterly'), (3, 'Biannually'), (4, 'Annually')])),
                ('transaction_type', models.IntegerField(choices=[(1, 'Deposit'), (2, 'Withdrawl'), (3, 'Transfer')])),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.Category')),
                ('dst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opposing_recurring_transactions', to='finance.Account')),
                ('src', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.Account')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Split',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(default=datetime.date.today)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_transactions', to='finance.Account')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='splits', to='finance.Category')),
                ('opposing_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_transactions', to='finance.Account')),
            ],
            options={
                'ordering': ['-date', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('date', models.DateField(default=datetime.date.today)),
                ('notes', models.TextField(blank=True, null=True)),
                ('transaction_type', models.IntegerField(choices=[(1, 'Deposit'), (2, 'Withdrawl'), (3, 'Transfer'), (4, 'Reconcile')])),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('recurrence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recurrences', to='finance.RecurringTransaction')),
            ],
            options={
                'ordering': ['-date', 'title'],
            },
        ),
        migrations.AddField(
            model_name='split',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='splits', to='finance.Transaction'),
        ),
        migrations.AddField(
            model_name='budget',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.Category'),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together={('name', 'account_type')},
        ),
    ]