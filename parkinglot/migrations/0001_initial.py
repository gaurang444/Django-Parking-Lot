# Generated by Django 2.2.11 on 2021-09-28 08:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingLot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parking_slot_name', models.CharField(blank=True, max_length=255, null=True)),
                ('parking_slot_adress', models.CharField(blank=True, max_length=255, null=True)),
                ('manager_name', models.CharField(blank=True, max_length=255, null=True)),
                ('manager_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('is_Active', models.BooleanField(blank=True, default=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_number', models.CharField(blank=True, max_length=30, null=True)),
                ('driving_license', models.CharField(blank=True, max_length=30, null=True)),
                ('system_entry', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_type', models.CharField(blank=True, choices=[('TWO WHEELER', 'TWO WHEELER'), ('FOUR WHEELER', 'FOUR WHEELER')], max_length=30, null=True)),
                ('is_Occupied', models.BooleanField(blank=True, default=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('vehicle_list', models.ManyToManyField(blank=True, null=True, to='parkinglot.Vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Ratecard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_type', models.CharField(blank=True, choices=[('TWO WHEELER', 'TWO WHEELER'), ('FOUR WHEELER', 'FOUR WHEELER')], max_length=30, null=True)),
                ('start_hour', models.IntegerField(blank=True, null=True)),
                ('end_hour', models.IntegerField(blank=True, null=True)),
                ('pricing', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('parking_lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkinglot.ParkingLot')),
            ],
        ),
        migrations.AddField(
            model_name='parkinglot',
            name='spot_list',
            field=models.ManyToManyField(blank=True, null=True, to='parkinglot.Spot'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parking_lot_entry_time', models.DateTimeField()),
                ('parking_lot_exit_time', models.DateTimeField()),
                ('booking_created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('pricing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkinglot.Ratecard')),
                ('spot_used', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkinglot.Spot')),
                ('vehicle_used', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parkinglot.Vehicle')),
            ],
        ),
    ]
