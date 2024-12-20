# Generated by Django 5.1.3 on 2024-12-06 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('type', models.CharField(choices=[('private_office', 'Private Office'), ('meeting_room', 'Meeting Room'), ('hot_desk', 'Hot Desk')], max_length=50)),
                ('capacity', models.PositiveIntegerField()),
                ('price_per_hour', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
    ]
