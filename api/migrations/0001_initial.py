# Generated by Django 4.0.5 on 2022-08-22 15:48

import api.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30, unique=True)),
                ('phone', models.CharField(max_length=30, null=True)),
                ('mobile', models.CharField(max_length=30, null=True)),
                ('company_name', models.CharField(max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('existing', models.BooleanField(default=False)),
                ('sales_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('SIGNED', 'SIGNED'), ('APPROVED', 'APPROVED'), ('CLOSED', 'CLOSED'), ('CANCELLED', 'CANCELLED'), ('EXPIRED', 'EXPIRED')], max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_due', models.DateField(validators=[api.validators.validate_date_not_in_past])),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='api.client')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=50, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('PROCESSING', 'PROCESSING'), ('UPCOMING', 'UPCOMING'), ('ONGOING', 'ONGOING'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED')], max_length=10)),
                ('attendees', models.IntegerField()),
                ('event_date_time', models.DateTimeField(null=True)),
                ('notes', models.CharField(max_length=255, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.client')),
                ('contract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='api.contract')),
                ('support_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
