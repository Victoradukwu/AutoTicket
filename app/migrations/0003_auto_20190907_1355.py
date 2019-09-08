# Generated by Django 2.1.7 on 2019-09-07 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20190829_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='status',
            field=models.IntegerField(choices=[(1, 'active'), (0, 'cancelled')], default=1),
        ),
        migrations.AlterField(
            model_name='seat',
            name='seat_number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='seat',
            name='status',
            field=models.IntegerField(choices=[(1, 'available'), (0, 'booked')], default=1),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='payment_status',
            field=models.IntegerField(choices=[(1, 'paid'), (0, 'pending')], default=1),
        ),
    ]