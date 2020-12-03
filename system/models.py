from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Classes
class Classes(models.Model):
    classes = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'classes'

    def __str__(self):
        return self.classes

# Subject


class Subject(models.Model):
    subject = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'subjects'

    def __str__(self):
        return self.subject

# Students


class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    family = models.IntegerField()
    fname = models.CharField(max_length=100)
    studentClass = models.ForeignKey(
        Classes, on_delete=models.CASCADE, default='1')
    section = models.CharField(max_length=10, blank=True)
    fees = models.CharField(max_length=6)
    contact = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    admissionDate = models.DateField()
    STATUS = [
        ('Active', 'active'),
        ('Left', 'left')
    ]
    status = models.CharField(max_length=6, choices=STATUS, default='Active')

    class Meta:
        db_table = 'students'

    def __str__(self):
        return self.user.first_name

# Teachers


class Teachers(models.Model):
    name = models.CharField(max_length=100)
    classes = models.ManyToManyField(Classes)
    subjects = models.ManyToManyField(Subject)
    joiningDate = models.DateField()
    contact = models.CharField(max_length=12, null=True, blank=True)
    salary = models.IntegerField()
    SALARY_STATUS = [
        ('P', 'paid'),
        ('U', 'unpaid')
    ]
    salaryStatus = models.CharField(
        max_length=6, choices=SALARY_STATUS, default='Unpaid')
    STATUS = [
        ('Active', 'active'),
        ('Left', 'left')
    ]
    status = models.CharField(max_length=6, choices=STATUS, default='Active')

    class Meta:
        db_table = 'teachers'

    def __str__(self):
        return self.name


# Incharge

class Incharge(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_incharge = models.BooleanField()

# Fees


class StudentFees(models.Model):
    students = models.ForeignKey(
        Students, on_delete=models.CASCADE, default='')
    feeMonth = models.CharField(max_length=20, blank=True, null=True)
    feeYear = models.CharField(max_length=4, blank=True, null=True)
    feeDate = models.DateField(blank=True, null=True)
    FEE_STATUS = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid')
    ]
    feeStatus = models.CharField(
        max_length=6, choices=FEE_STATUS, default='Unpaid')

    class Meta:
        db_table = 'fees'

    def __str__(self):
        return self.feeStatus

    @property
    def Month(self):
        if self.Date:
            return self.Date.strftime("%B")
        return ""

# Attendense


class Attendense(models.Model):
    student = models.ForeignKey(
        Students, on_delete=models.CASCADE, default='')
    ATTENDENCE = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave')
    ]
    attendence = models.CharField(
        max_length=7, choices=ATTENDENCE, default="Present")
    date = models.DateField()
    month = models.CharField(max_length=20, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        db_table = 'attendence'

    def __str__(self):
        return self.attendence


# Expense

class Expense(models.Model):
    amount = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    date = models.DateField(auto_now_add=True)
    month = models.CharField(max_length=20, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return self.desc

    
# Income

class Income(models.Model):
    amount = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    date = models.DateField(auto_now_add=True)
    month = models.CharField(max_length=20, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return self.desc

# balance 

class Balance(models.Model):
    balance = models.IntegerField()
    month = models.CharField(max_length=20, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)

    def save(self):
        # count will have all of the objects from the Aboutus model
        count = Balance.objects.all().count()
        # this will check if the variable exist so we can update the existing ones
        save_permission = Balance.has_add_permission(self)

        # if there's more than two objects it will not save them in the database
        if count < 2:
            super(Balance, self).save()
        elif save_permission:
            super(Balance, self).save()

    def has_add_permission(self):
        return Balance.objects.filter(id=self.id).exists()


class Header(models.Model):
    img = models.ImageField(upload_to='images/')

class Documents(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.document.delete()
        super().delete(*args, **kwargs)  


class Test(models.Model):
    student = models.ForeignKey(
        Students, on_delete=models.CASCADE, default='')
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, default='')
    obtainedMarks = models.IntegerField()
    totalMarks = models.IntegerField()
    date = models.DateField(blank=True, null=True)