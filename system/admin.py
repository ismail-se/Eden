from django.contrib import admin
from .models import Classes, Subject, Students, Teachers, StudentFees, Income, Expense, Attendense

# Register your models here.
admin.site.register(Classes)
admin.site.register(Subject)
admin.site.register(Students)
admin.site.register(Teachers)
admin.site.register(StudentFees)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Attendense)
