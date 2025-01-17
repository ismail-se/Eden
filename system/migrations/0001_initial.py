# Generated by Django 3.1.3 on 2020-11-04 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classes', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'classes',
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=300)),
                ('date', models.DateField(auto_now_add=True)),
                ('month', models.CharField(blank=True, max_length=20, null=True)),
                ('year', models.CharField(blank=True, max_length=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Header',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=300)),
                ('date', models.DateField(auto_now_add=True)),
                ('month', models.CharField(blank=True, max_length=20, null=True)),
                ('year', models.CharField(blank=True, max_length=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'db_table': 'subjects',
            },
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('joiningDate', models.DateField()),
                ('contact', models.CharField(blank=True, max_length=12, null=True)),
                ('salary', models.IntegerField()),
                ('salaryStatus', models.CharField(choices=[('P', 'paid'), ('U', 'unpaid')], default='Unpaid', max_length=6)),
                ('status', models.CharField(choices=[('Active', 'active'), ('Left', 'left')], default='Active', max_length=6)),
                ('classes', models.ManyToManyField(to='system.Classes')),
                ('subjects', models.ManyToManyField(to='system.Subject')),
            ],
            options={
                'db_table': 'teachers',
            },
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('family', models.IntegerField()),
                ('fname', models.CharField(max_length=100)),
                ('section', models.CharField(blank=True, max_length=10)),
                ('fees', models.CharField(max_length=6)),
                ('contact', models.CharField(blank=True, max_length=12, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('admissionDate', models.DateField()),
                ('status', models.CharField(choices=[('Active', 'active'), ('Left', 'left')], default='Active', max_length=6)),
                ('studentClass', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='system.classes')),
            ],
            options={
                'db_table': 'students',
            },
        ),
        migrations.CreateModel(
            name='StudentFees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feeMonth', models.CharField(blank=True, max_length=20, null=True)),
                ('feeYear', models.CharField(blank=True, max_length=4, null=True)),
                ('feeDate', models.DateField(blank=True, null=True)),
                ('feeStatus', models.CharField(choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid', max_length=6)),
                ('students', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='system.students')),
            ],
            options={
                'db_table': 'fees',
            },
        ),
        migrations.CreateModel(
            name='Attendense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendence', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')], default='Present', max_length=7)),
                ('date', models.DateField()),
                ('student', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='system.students')),
            ],
            options={
                'db_table': 'attendence',
            },
        ),
    ]
