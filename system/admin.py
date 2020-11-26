from django.contrib import admin
from .models import Classes, Subject, Students, Teachers, Incharge, StudentFees, Income, Expense, Attendense, Test

# Register your models here.
admin.site.register(Classes)
admin.site.register(Subject)
admin.site.register(Students)
admin.site.register(Teachers)
admin.site.register(Incharge)
admin.site.register(StudentFees)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Attendense)
admin.site.register(Test)
