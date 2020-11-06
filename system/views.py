from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Classes, Subject, Students, Teachers, StudentFees, Income, Expense, Balance, Header
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.sessions.models import Session
from .forms import *
import datetime
import os 
import sys 
import csv
import pandas as pd 
import random
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from dateutil.relativedelta import relativedelta


# Create your views here.


def index(request):
    if (not request.user.is_anonymous):
        if request.user.is_superuser:
            return redirect("/home")
        else:
            std = Students.objects.get(user=request.user)
            if std.status == "Active":
                return redirect('/student-dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/home')
            else:
                return redirect('/student-dashboard')
        else:
            messages.error(
                request, "You entered incorrect username or password")
            return render(request, 'signin.html')

    return render(request, 'signin.html')


def logoutUser(request):
    logout(request)
    return redirect("/")


def home(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")
    students = Students.objects.filter(status = "Active")
    fees = StudentFees.objects.all()
    x = datetime.datetime.now()
    month = x.strftime("%B")
    year = x.strftime("%Y")
    day = x.strftime("%d")
    

    # expense = Expense.objects.filter(month=month, year=year)
    # income = Income.objects.filter(month=month, year=year)
    b,c = Balance.objects.get(pk=1)
    flag = 0
    if (day == '01'):
        for f in fees:
            if f.feeMonth == month and f.feeYear == year:
                flag == 1
                break
        if b.balance == 0:
            last_month = datetime.now() - relativedelta(months=1)
            lmonth = last_month.strftime("%B")
            lyear = last_month.strftime("%Y")
            income = Income.objects.filter(month=lmonth, year=lyear)
            bal = 0
            for i in income:
                bal += i.amount
            b.balance = bal
            b.save()

    if flag == 0:
        for s in students:
            fee = StudentFees(students=s, feeMonth=month, feeYear=year, feeStatus="Unpaid")
        

    
        
    return render(request, "home.html")


def dashboard(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")

    students = Students.objects.filter(status = "Active")
    fees = StudentFees.objects.all()
    student_fees = 0
    def_students = {}
    def_students_list = []
    month = []
    totalFee = 0

    for student in students:
        totalFee += int(student.fees)
        
        for fee in fees:
            if fee.feeMonth not in month:
                month.append(fee.feeMonth)
            if student.user.id == fee.students.user.id:
                if str(student.user.id) in def_students:
                    def_students[str(student.user.id)][fee.feeMonth] = fee.feeStatus
                else:
                    def_students[str(student.user.id)] = {
                        fee.feeMonth:fee.feeStatus 
                    }
                    for f in StudentFees.objects.filter(students=Students.objects.get(pk=student.user.id)): 
                        if f.feeStatus == 'Unpaid':
                            if student not in def_students_list:
                                def_students_list.append(Students.objects.get(pk=student.user.id))
                    
    month.reverse()
    month1 = []
    for i in range(12):
        try:
            month1.append(month[i])
        except:
            break

    
    for key in def_students:
        for mon in month1:
            if mon not in def_students[key]:
                def_students[key][mon] = "None"
    
    x = datetime.datetime.now()
    month = x.strftime("%B")
    year = x.strftime("%Y")

    expense = Expense.objects.filter(month=month, year=year)
    income = Income.objects.filter(month=month, year=year)
    # Expense
    totalExp = 0
    for e in expense:
        totalExp += int(e.amount)
    # Income
    totalInc = 0
    for i in income:
        totalInc += int(i.amount)

    

    fee = StudentFees.objects.filter(feeMonth=month, feeStatus="Paid")
    feeInc = 0
    for f in fee:
        feeInc += int(f.students.fees)
    totalInc += feeInc


    profit = totalInc - totalExp


    context = {
        'defaulters': len(def_students_list),
        'totalStudents': len(students),
        'totalTeachers': len(Teachers.objects.all()),
        'totalExp': totalExp,
        'totalInc': totalInc,
        'students': def_students_list,
        'month': month1,
        'def': def_students,
        'totalFee': totalFee,
        'profit': profit,
    }
    return render(request, "dashboard.html", context)


def students(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")

    students = Students.objects.all()
    fees = StudentFees.objects.all()
    def_students = {}
    def_students_list = []
    month = []

    for student in students:
        for fee in fees:
            if fee.feeMonth not in month:
                month.append(fee.feeMonth)
            if student.user.id == fee.students.user.id:
                if str(student.user.id) in def_students:
                    def_students[str(student.user.id)][fee.feeMonth] = fee.feeStatus
                else:
                    def_students[str(student.user.id)] = {
                        fee.feeMonth:fee.feeStatus 
                    }
                    for f in StudentFees.objects.filter(students=Students.objects.get(pk=student.user.id)): 
                        if f.feeStatus == 'Unpaid':
                            if student not in def_students_list:
                                def_students_list.append(Students.objects.get(pk=student.user.id))
                    
    month.reverse()
    month1 = []
    for i in range(12):
        try:
            month1.append(month[i])
        except:
            break

    
    for key in def_students:
        for mon in month1:
            if mon not in def_students[key]:
                def_students[key][mon] = "None"

    students = Students.objects.all()
    context = {
        'students': students,
        'def': def_students,
        'month': month1,
        'len': len(students),
    }
    return render(request, "students.html", context)


def registerStudents(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")

    if request.method == "POST":        
        
        family = request.POST.get('family')
        name = request.POST.get('name')
        fname = request.POST.get('fname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password, first_name=name)
        user.save()
        studentClass = request.POST.get('class')
        section = request.POST.get('section')
        fees = request.POST.get('fees')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        x = datetime.datetime.now()
        newStudent = Students(user=user, family=family, fname=fname, studentClass=Classes.objects.get(
            pk=studentClass), section=section, fees=fees, contact=contact, address=address, admissionDate=x.strftime('%Y'+'-'+'%m'+'-'+'%d'))
        newStudent.save()
        messages.success(request, "Student has registered successfully")

        newFee = StudentFees(feeMonth=x.strftime("%B"), feeDate=x.strftime(
            '%Y'+'-'+'%m'+'-'+'%d'), feeStatus='Unpaid', students=newStudent)
        newFee.save()

    classes = Classes.objects.all().order_by('classes')
    students = Students.objects.all()
    max_family = 1
    for s in students:
        if s.family > max_family:
            max_family = s.family

    context = {
        'classes': classes,
        'students': students,
        'password': random.randint(100000,999999),
        "family": int(max_family)+1,
    }
    return render(request, "register-student.html", context)

def deleteStudents(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")
    
    students = Students.objects.all()
    fees = StudentFees.objects.all()
    def_students = {}
    def_students_list = []
    month = []

    for student in students:
        for fee in fees:
            if fee.feeMonth not in month:
                month.append(fee.feeMonth)
            if student.user.id == fee.students.user.id:
                if str(student.user.id) in def_students:
                    def_students[str(student.user.id)][fee.feeMonth] = fee.feeStatus
                else:
                    def_students[str(student.user.id)] = {
                        fee.feeMonth:fee.feeStatus 
                    }
                    for f in StudentFees.objects.filter(students=Students.objects.get(pk=student.user.id)): 
                        if f.feeStatus == 'Unpaid':
                            if student not in def_students_list:
                                def_students_list.append(Students.objects.get(pk=student.user.id))
                    
    month.reverse()
    month1 = []
    for i in range(12):
        try:
            month1.append(month[i])
        except:
            break

    
    for key in def_students:
        for mon in month1:
            if mon not in def_students[key]:
                def_students[key][mon] = "None"


    students = Students.objects.all()
    context = {
        'students': students,
        'def': def_students,
        'month': month1,
    }
    return render(request, "delete-student.html", context)

def deleteFee(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")
    
    students = Students.objects.all()
    fees = StudentFees.objects.all()
    def_students = {}
    def_students_list = []
    month = []

    for student in students:
        for fee in fees:
            if fee.feeMonth not in month:
                month.append(fee.feeMonth)
            if student.user.id == fee.students.user.id:
                if str(student.user.id) in def_students:
                    def_students[str(student.user.id)][fee.feeMonth] = fee.feeStatus
                else:
                    def_students[str(student.user.id)] = {
                        fee.feeMonth:fee.feeStatus 
                    }
                    for f in StudentFees.objects.filter(students=Students.objects.get(pk=student.user.id)): 
                        if f.feeStatus == 'Unpaid':
                            if student not in def_students_list:
                                def_students_list.append(Students.objects.get(pk=student.user.id))
                    
    month.reverse()
    month1 = []
    for i in range(12):
        try:
            month1.append(month[i])
        except:
            break

    
    for key in def_students:
        for mon in month1:
            if mon not in def_students[key]:
                def_students[key][mon] = "None"


    students = Students.objects.all()
    context = {
        'students': students,
        'def': def_students,
        'month': month1,
        'fees': fees,
    }
    return render(request, "delete-fee.html", context)

def updateStudents(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")

    if request.method == "POST":
        id = request.POST.get('id')
        family = request.POST.get('family')
        name = request.POST.get('name')
        fname = request.POST.get('fname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        studentClass = request.POST.get('class')
        section = request.POST.get('section')
        fees = request.POST.get('fees')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        status = request.POST.get('status')
        x = datetime.datetime.now()
        newUser = User.objects.get(pk=id)
        newUser.username = username
        if password != "":
            newUser.password = password
        newUser.first_name = name
        newStudent = Students.objects.get(user=newUser)
        newStudent.family = family
        newStudent.fname = fname
        newStudent.studentClass=Classes.objects.get(id=studentClass)
        newStudent.section = section
        newStudent.fees = fees
        newStudent.contact = contact
        newStudent.address = address
        newStudent.status = status
        newUser.save()
        newStudent.save()

        messages.success(request, "Student has updated successfully")


    classes = Classes.objects.all().order_by('classes')
    students = Students.objects.all()
    context = {
        'classes': classes,
        'students': students
    }
    return render(request, "update-student.html", context)

def registerTeacher(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")

    if request.method == "POST":
        name = request.POST.get('name')
        salary = request.POST.get('salary')
        contact = request.POST.get('contact')
        selectedClass = request.POST.getlist('class')
        selectedSubject = request.POST.getlist('subject')

        x = datetime.datetime.now()
        newTeacher = Teachers(name=name, joiningDate=x.strftime(
            '%Y'+'-'+'%m'+'-'+'%d'), contact=contact, salary=salary)
        newTeacher.save()
        for i in selectedClass:
            newTeacher.classes.add(Classes.objects.get(classes=i))
        for i in selectedSubject:
            newTeacher.subjects.add(Subject.objects.get(subject=i))
        messages.success(request, "Teacher has registered successfully")

    classes = Classes.objects.all().order_by("classes")
    subjects = Subject.objects.all().order_by("subject")
    context = {
        'classes': classes,
        'subjects': subjects,
    }
    return render(request, "register-teacher.html", context)

def updateTeacher(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")

    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        salary = request.POST.get('salary')
        contact = request.POST.get('contact')
        selectedClass = request.POST.getlist('class')
        selectedSubject = request.POST.getlist('subject')
        newTeacher = Teachers.objects.get(pk=id)
        newTeacher.name = name
        newTeacher.salary = salary
        newTeacher.contact = contact
        newTeacher.save()

        cl = newTeacher.classes.all()
        sb = newTeacher.subjects.all()

        for c in cl:
            newTeacher.classes.remove(c)
        for s in sb:
            newTeacher.subjects.remove(s)
        
        for i in selectedClass:
            newTeacher.classes.add(Classes.objects.get(classes=i))
        for i in selectedSubject:
            newTeacher.subjects.add(Subject.objects.get(subject=i))

        messages.success(request, "Teacher has updated successfully")


    classes = Classes.objects.all().order_by('classes')
    subjects = Subject.objects.all().order_by("subject")
    context = {
        'classes': classes,
        'subjects': subjects,
    }
    return render(request, "update-teacher.html", context)

def deleteTeacher(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")

    teachers = Teachers.objects.all()
    context = {
        'teachers': teachers,
    }
    return render(request, "delete-teacher.html", context)

def teachers(request):
    if request.user.is_anonymous:
        return redirect("/")

    teachers = Teachers.objects.all()
    context = {
        'teachers': teachers,
        'length': len(teachers)
    }
    return render(request, "teachers.html", context)


def classes(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")

    if request.method == "POST":
        myclass = request.POST.get('classes')
        newClass = Classes(classes=myclass)
        newClass.save()
        return redirect("/classes")

    classes = Classes.objects.all().order_by('classes')
    context = {
        'classes': classes,
        'length': len(classes)
    }
    return render(request, "classes.html", context)


def subjects(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")

    if request.method == "POST":
        subject = request.POST.get('subjects')
        newSubject = Subject(subject=subject)
        newSubject.save()
        return redirect("/subjects")

    subjects = Subject.objects.all()
    context = {
        'subjects': subjects,
        'length': len(subjects)
    }
    return render(request, "subjects.html", context)


def fees(request):
    if request.user.is_anonymous and not request.user.is_superuser:
        return redirect("/")

    students = Students.objects.filter(status = "Active")
    fees = StudentFees.objects.all()
    def_students = {}
    def_students_list = []
    month = []
    ye =[]

    for student in students:
        for fee in fees:
            if fee.feeMonth not in month:
                month.append(fee.feeMonth)
            if fee.feeYear not in ye:
                ye.append(fee.feeYear)
            if student.user.id == fee.students.user.id:
                if str(student.user.id) in def_students:
                    def_students[str(student.user.id)][fee.feeMonth] = fee.feeStatus
                else:
                    def_students[str(student.user.id)] = {
                        fee.feeMonth:fee.feeStatus 
                    }
                    for f in StudentFees.objects.filter(students=Students.objects.get(pk=student.user.id)): 
                        if f.feeStatus == 'Unpaid':
                            if student not in def_students_list:
                                def_students_list.append(Students.objects.get(pk=student.user.id))
                    
    month.reverse()
    month1 = []
    for i in range(12):
        try:
            month1.append(month[i])
        except:
            break

    
    for key in def_students:
        for mon in month1:
            if mon not in def_students[key]:
                def_students[key][mon] = "None"

    if request.method == "POST":
        if request.POST.get('payFee') != None:
            student = []
            studentName = []
            studentFees = []
            studentClass = []
            user = User.objects.get(pk=request.POST.get('payFee'))
            std = Students.objects.get(user=user)
            student.append(std.user.id)
            studentName.append(std.user.first_name)
            studentFees.append(std.fees)
            studentClass.append(std.studentClass.classes)
            month = request.POST.getlist('monthFee')
            year = request.POST.get('year')

            sameFamily = request.POST.getlist('sameFamily')

            for i in sameFamily:
                std = Students.objects.get(pk=int(i))
                student.append(std.user.id)
                studentName.append(std.user.first_name)
                studentFees.append(std.fees)
                studentClass.append(std.studentClass.classes)
            
            for i in month:
                for j in student:
                    s = Students.objects.get(pk=j)
                    x = datetime.datetime.now()
                    newFees = StudentFees.objects.get_or_create(students = s, feeMonth = i, feeYear=year)
                    newFees[0].feeStatus = "Paid"
                    newFees[0].feeDate = x.strftime("%Y-%m-%d")

                    newFees[0].save()
            
                
            
            tStudentFees = list(map(lambda x: int(x)*len(month), studentFees))
            
            
            request.session['name'] = studentName
            request.session['class'] = studentClass
            request.session['fees'] = tStudentFees
            request.session['month'] = month 
            request.session['anotherFee'] = request.POST.get('anotherFee')
            request.session['selectFee'] = request.POST.get('selectFee')
            

        return redirect("/fee-receipt")
    
    students = Students.objects.filter(status="Active")
    
    context = {
        'students': students,
        'def': def_students,
        'month': month1,
        'year': ye,
    }
    return render(request, "fees.html", context)

def feeReceipt(request):
    if request.user.is_anonymous and not request.user.is_superuser:
        return redirect("/")
    
    header = Header.objects.all()
    h = ''
    for i in header:
        h = i
    x = datetime.datetime.now()
    name = classes = fees = month = anotherFee = selectFee = ''
    if request.session.has_key('name'):
        name = request.session['name'] 
        classes = request.session['class'] 
        fees = request.session['fees'] 
        month = request.session['month'] 
        anotherFee = request.session['anotherFee'] 
        selectFee = ''
        if anotherFee != "":
            selectFee = request.session['selectFee'] 
            
    context = {
        'name':name,
        'class':classes,
        'fees':fees,
        'month': month,
        'anotherFee':anotherFee,
        'selectFee':selectFee,
        'date': x.strftime('%d'+'-'+'%b'+'-'+'%y'),
        'header': h,
    }
    return render(request, "fee-receipt.html", context)

def attendence(request):
    if request.user.is_anonymous and not request.user.is_superuser:
        return redirect("/")
    
    stdClasses = Classes.objects.all()
    students = Students.objects.filter(status="Active")
    attendence = Attendense.objects.all()
    att = {}
    attDate = []
    monthNo = []
    months = [0, "January", "Febraury", "March", "April", "May", "June", "July", "August", "September", "October", "Novemer", "December"]
    mon = []

    for a in attendence:
        
        if a.date not in attDate:
            attDate.append(a.date)
        
        m = a.date.month
        if months[m] not in mon:
            mon.append(months[m])
        
    for a in attendence:
        if a.student.status == "Active":
            if a.student.user.id not in att:
                att[a.student.user.id] = {
                        "name":a.student.user.first_name,
                        "class":a.student.studentClass,
                    }
                for at in attDate:
                    att[a.student.user.id][at] = "-"

                att[a.student.user.id][a.date] = a.attendence
            else:
                att[a.student.user.id][a.date] = a.attendence
            
        # if a.date.month == datetime.datetime.now().month:
        #     pass

    context = {
        "classes": stdClasses,
        "attendenceDate":attDate,
        "attendence": att,
        "mon": mon,
    }
    return render(request, "attendence.html", context)

def addAttendence(request):
    if request.user.is_anonymous and not request.user.is_superuser:
        return redirect("/")
    
    if request.method == 'POST':
        classes = request.POST.get('class')
        stdClass = Classes.objects.get(pk=classes)
        std = Students.objects.filter(studentClass=stdClass, status="Active")
        date = request.POST.get('date')

        for s in std:
            try:
                att = Attendense.objects.get(student=s, date=date)
                attendence = request.POST.get(str(s.user.id))
                att.attendence=attendence
                att.save()
            except:
                attendence = request.POST.get(str(s.user.id))
                att = Attendense(student=s, date=date, attendence=attendence)
                att.save()

    stdClasses = Classes.objects.all()
    students = Students.objects.filter(status = "Active")
    context = {
        "classes": stdClasses,
        "students": students,
    }
    return render(request, "add-attendence.html", context)

def changeAttendence(request):
    stdClass = request.GET.get('class', None)
    id = []
    name = []
    classes = Classes.objects.get(pk=stdClass)
    std = Students.objects.filter(studentClass = classes, status="Active")
    for s in std:
        id.append(s.user.id)
        name.append(s.user.first_name)
    data = {
        "id":id,
        "name":name,
    }
    return JsonResponse(data)

def income(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")
    x = datetime.datetime.now()
    if request.method == "POST":
        amount = request.POST.get('amount')
        desc = request.POST.get('desc')
        inc = Income(amount=amount, desc=desc, month=x.strftime("%B"), year=x.strftime("%Y"))
        inc.save()
        return redirect("/income")

    x = datetime.datetime.now()
    month = x.strftime("%B")
    year = x.strftime("%Y")

    income = Income.objects.filter(month=month, year=year)
    total = 0
    for inc in income:
        total += int(inc.amount)

    bal = 0
    if Balance.objects.all().count() < 1:
        bal = Balance(balance=0, id=1)
        bal.save()
    else:
        bal = Balance.objects.get(pk=1)
    context = {
        'income': income,
        'balance': bal.balance,
        'length': total
    }
    return render(request, "income.html", context)


def expense(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")
    x = datetime.datetime.now()
    if request.method == "POST":
        amount = request.POST.get('amount')
        desc = request.POST.get('desc')
        exp = Expense(amount=amount, desc=desc, month=x.strftime("%B"), year=x.strftime("%Y"))
        exp.save()
        return redirect("/expense")

    month = x.strftime("%B")
    year = x.strftime("%Y")

    expense = Expense.objects.filter(month=month, year=year)
    total = 0
    for exp in expense:
        total += int(exp.amount)
    context = {
        'expense': expense,
        'length': total
    }
    return render(request, "expense.html", context)


def reports(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")
    x = datetime.datetime.now() 
    month = x.strftime("%B")
    year = x.strftime("%Y")
    income = Income.objects.all()
    inc_total = 0
    for inc in income:
        inc_total += int(inc.amount)
    
    expense = Expense.objects.all()
    exp_total = 0
    for exp in expense:
        exp_total += int(exp.amount)

    students = Students.objects.all()
    fees = StudentFees.objects.all()
    def_students = {}
    def_students_list = []
    month = []
    totalFee = 0

    for student in students:
        totalFee += int(student.fees)
        for fee in fees:
            if fee.feeMonth not in month:
                month.append(fee.feeMonth)
            if student.user.id == fee.students.user.id:
                if str(student.user.id) in def_students:
                    def_students[str(student.user.id)][fee.feeMonth] = fee.feeStatus
                else:
                    def_students[str(student.user.id)] = {
                        fee.feeMonth:fee.feeStatus 
                    }
                    for f in StudentFees.objects.filter(students=Students.objects.get(pk=student.user.id)): 
                        if f.feeStatus == 'Unpaid':
                            if student not in def_students_list:
                                def_students_list.append(Students.objects.get(pk=student.user.id))
                    
    month.reverse()
    month1 = []
    for i in range(12):
        try:
            month1.append(month[i])
        except:
            break

    # Expense
    totalExp = 0
    for e in expense:
        totalExp += int(e.amount)
    # Income
    totalInc = 0
    for i in income:
        totalInc += int(i.amount)

    x = datetime.datetime.now()
    month = x.strftime("%B")

    fee = StudentFees.objects.filter(feeMonth=month, feeStatus="Paid")
    feeInc = 0
    for f in fee:
        feeInc += int(f.students.fees)
    totalInc += feeInc


    context = {
        'income': income,
        'length': inc_total,
        'expense': expense,
        'length': exp_total,
        'students': students,
        'totalStudents': len(students),
        'totalInc':totalInc,
        'totalExp':totalExp,
        'def': def_students,
        'month': month1,
    }
    return render(request, "reports.html", context)


def settings(request):
    if request.user.is_anonymous:
        return redirect("/")

    if request.method == 'POST':
        newUsername = request.POST.get('username')
        newPassword = request.POST.get('password')
        repeatPassword = request.POST.get('repeatPassword')
        username = request.user.username

        if newPassword == repeatPassword:

            user = User.objects.get(username=username)
            user.username = newUsername
            user.set_password(newPassword)
            user.save()
            messages.success(
                request, "Username and password changed successfully")
            logout(request)

    return render(request, "settings.html")

def documents(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('documents')
    else:
        form = DocumentForm()

    docs = Documents.objects.all()

    context = {
        'form': form,
        'docs': docs,
        }

    return render(request, "documents.html", context)

def importCSV(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect("/")

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES['file'])
            df = pd.read_csv (request.FILES['file'])
            x = datetime.datetime.now()
            month = x.strftime("%B")
            year = x.strftime("%Y")
            for i in range(len(df.index)):
                print(df.at[i, 'name'])
                user = User(
                    username=df.at[i, 'username'],
                    password=df.at[i, 'password'],
                    first_name=df.at[i, 'name'],
                    )
                user.save()
                studntClass = Classes.objects.get(classes=df.at[i, 'class'])
                std = Students(
                    user=user,
                    family=df.at[i, 'family_no'],
                    fname=df.at[i, 'fname'],
                    studentClass=studntClass,
                    fees=df.at[i, 'fees'],
                    contact=df.at[i, 'contact'],
                    admissionDate=x.strftime("%Y-%m-%d"),
                    status=df.at[i, 'status'],
                )
                std.save()
                fees = StudentFees(students=std, feeMonth=month, feeYear=year, feeStatus="Unpaid")
                fees.save()
                return redirect("/students")
    else:
        form = UploadFileForm()


    return render(request, "import-students.html", {'form': form})

def checkFamily(request):
    family = int(request.GET.get('family', None))
    students = Students.objects.all()
    address = ""
    contact = ""
    for student in students:
        if student.family == family:
            address = student.address
            contact = student.contact

    data = {
        'address': address,
        'contact': contact,
    }
    return JsonResponse(data)


def clearExp(request):
    expense = Expense.objects.all()
    for e in expense:
        e.delete()
    data = {}
    return JsonResponse(data)


def clearInc(request):
    income = Income.objects.all()
    for e in income:
        e.delete()
    data = {}
    return JsonResponse(data)


def clearBalance(request):
    b = Balance.objects.get(pk=1)
    b.balance = 0
    b.save()
    data = {}
    return JsonResponse(data)


def itoc(request):
    income = Income.objects.all()
    b = Balance.objects.get(pk=1)

    for e in income:
        b.balance += int(e.amount)
    b.save()

    for e in income:
        e.delete()

    data = {}
    return JsonResponse(data)


def subjectDelete(request):
    id = request.GET.get('id', None)
    b = Subject.objects.get(pk=id)
    b.delete()
    data = {}
    return JsonResponse(data)



def classDelete(request):
    id = request.GET.get('id', None)
    b = Classes.objects.get(pk=id)
    b.delete()
    data = {}
    return JsonResponse(data)


def stdDelete(request):
    id = int(request.GET.get('id', None))
    user = User.objects.get(pk=id)
    std = Students.objects.get(user=user)
    std.delete()
    user.delete()
    data = {}
    return JsonResponse(data)

def feeDelete(request):
    id = int(request.GET.get('id', None))
    fee = StudentFees.objects.get(pk=id)
    fee.delete()
    data = {}
    return JsonResponse(data)

def incDelete(request):
    id = int(request.GET.get('id', None))
    inc = Income.objects.get(pk=id)
    inc.delete()
    data = {}
    return JsonResponse(data)

def expDelete(request):
    id = int(request.GET.get('id', None))
    exp = Expense.objects.get(pk=id)
    exp.delete()
    data = {}
    return JsonResponse(data)

def stdUpdate(request):
    id = int(request.GET.get('family', None))
    students = Students.objects.all()
    familyNo = ""
    name = ""
    fname = ""
    username = ""
    studentClass = ""
    section = ""
    fees = ""
    contact = ""
    address = ""
    
    for student in students:
        if student.user.id == id:
            familyNo = student.family
            name = student.user.first_name
            fname = student.fname
            username = student.user.username
            studentClass = student.studentClass.classes
            section = student.section
            fees = student.fees
            contact = student.contact
            address = student.address
            

    data = {
        'family': familyNo,
        'name': name,
        'fname': fname,
        'username': username,
        'studentClass': studentClass,
        'section': section,
        'fees': fees,
        'contact': contact,
        'address': address,
        
    }
    return JsonResponse(data)

def tecUpdate(request):
    id = int(request.GET.get('id', None))
    teachers = Teachers.objects.all()
    name = ""
    classes = ""
    subjects = ""
    contact = ""
    salary = ""
    
    for teacher in teachers:
        if teacher.id == id:
            name = teacher.name
            classes = list(teacher.classes.all())
            subjects = list(teacher.subjects.all())
            contact = teacher.contact
            salary = teacher.salary
      
    classes_json = serializers.serialize('json', classes)
    subjects_json = serializers.serialize('json', subjects)

    print(classes_json)
    print(subjects_json)

    data = {
        'name': name,
        'classes': classes_json,
        'subjects': subjects_json,
        'contact': contact,
        'salary': salary
    }
    
    return JsonResponse(data)

def tecDelete(request):
    id = request.GET.get('id', None)
    b = Teachers.objects.get(pk=id)
    b.delete()
    data = {}
    return JsonResponse(data)


def uploadHeader(request):
    if request.user.is_anonymous:
        return redirect("/")

    if request.method == 'POST':
        form = HeaderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/fees")
    else:
        form = HeaderForm()
    return render(request, "upload-header.html", {'form' : form})


def studentLogin(request):
    if request.method == 'POST':
        return redirect("/student-dashboard")
    return render(request, "student-login.html")

def studentDashboard(request):
    if request.user.is_anonymous:
        return redirect("/")

    students = Students.objects.get(user = request.user)
    attendence = Attendense.objects.filter(student=students)
    att = {}
    attDate = []
    monthNo = []
    months = [0, "January", "Febraury", "March", "April", "May", "June", "July", "August", "September", "October", "Novemer", "December"]
    mon = []

    for a in attendence:
        
        if a.date not in attDate:
            attDate.append(a.date)
        
        m = a.date.month
        if months[m] not in mon:
            mon.append(months[m])
     
    print(attendence)
    x = datetime.datetime.now()
    month = x.strftime("%B")
    fee = StudentFees.objects.filter(students=students)
    docs = Documents.objects.all()

    context = {
        "name": request.user.first_name,
        "attendenceDate":attDate,
        "attendence": attendence,
        "mon": mon,
        "fee": fee,
        "docs": docs,
    }
    return render(request, "student-dashboard.html", context)


def monthData(request):
    id = request.GET.get('id', None)
    m = request.GET.get('month', None)
    students = Students.objects.all()
    fees = StudentFees.objects.all()
    def_students = {}
    month = []

    for student in students:
        for fee in fees:
            if fee.feeMonth not in month:
                month.append(fee.feeMonth)
            if student.user.id == fee.students.user.id:
                if str(student.user.id) in def_students:
                    def_students[str(student.user.id)][fee.feeMonth] = fee.feeStatus
                else:
                    def_students[str(student.user.id)] = {
                        fee.feeMonth:fee.feeStatus 
                    }
                    
                    
    month.reverse()
    month1 = []
    for i in range(12):
        try:
            month1.append(month[i])
        except:
            break

    
    for key in def_students:
        for mon in month1:
            if mon not in def_students[key]:
                def_students[key][mon] = "None"
    
    data = {
        'val': def_students[id][m] 
    }
    
    return JsonResponse(data)

def delDocuments(request):
    id = request.GET.get('id', None)
    doc = Documents.objects.get(pk=id)
    doc.delete()
    
    data = {
        
    }
    
    return JsonResponse(data)

def usernameCheck(request):
    username = request.GET.get('username', None)
    flag = 1
    students = Students.objects.all()
    

    for student in students:
        if student.user.username == username:
            flag = 0
            break     
                    
    data = {
        'flag': flag
    }
    
    return JsonResponse(data)

def feeReceiptValue(request):
    i = request.GET.get('i', None)
    n = request.GET.get('n', None)
    
    name = request.session['name'] 
    classes = request.session['class'] 
    fees = request.session['fees'] 
    anotherFee = request.session['anotherFee'] 
    
    
    myName = name[int(i)]
    myClass = classes[int(i)]
    myFees = fees[int(i)]
    total = myFees
    if anotherFee != "":
        total = int(myFees)+int(anotherFee)
                       
    data = {
        'name': myName,
        'class': myClass,
        'fees': myFees,
        'total': total,
    }
    
    return JsonResponse(data)

def getFamily(request):
    family = request.GET.get('family', None)
    students = Students.objects.filter(family=family, status="Active")
    all_students = {}   
    for student in students:
        all_students[str(student.user.id)] = {
            'familyNo' : student.family,
            'name' : student.user.first_name,
            'fname' : student.fname,
            'username' : student.user.username,
            'studentClass' : student.studentClass.classes,
            'section' : student.section,
            'fees' : student.fees,
            'contact' : student.contact,
            'address' : student.address,
            'admissionDate': student.admissionDate,
            'status': student.status
        }
    
    

    data = {
        'all_students':all_students
    }
    
    return JsonResponse(data)

def contactDownload(request):
    con = request.GET.getlist('con[]')
    # mycsv = csv.writer(open(r'./media/contacts.csv', 'w'))
    
    # for data in con:
    #     mycsv.write(data+'\n')
    df = pd.DataFrame(data={"contacts": con})
    df.to_csv(r'./media/contacts.csv', sep=',',index=False)
    
    data = {}
    return JsonResponse(data)

def incomeDownload(request):
    
    month = request.GET.get('month', None)
    year = request.GET.get('year', None)
    
    income = Income.objects.filter(month=month, year=year)
    amount = []
    desc = []
    date = []
    for i in income:
        amount.append(i.amount)
        desc.append(i.desc)
        date.append(i.date)
   
    df = pd.DataFrame(data={"Amount": amount, "Description": desc, "Date": date})
    df.to_csv(r'./media/income.csv', sep=',',index=False)
    
    data = {}
    return JsonResponse(data)

def expenseDownload(request):
    month = request.GET.get('month', None)
    year = request.GET.get('year', None)
    expense = Expense.objects.filter(month=month, year=year)
    amount = []
    desc = []
    date = []
    for i in expense:
        amount.append(i.amount)
        desc.append(i.desc)
        date.append(i.date)
   
    df = pd.DataFrame(data={"Amount": amount, "Description": desc, "Date": date})
    df.to_csv(r'./media/expense.csv', sep=',',index=False)
    
    data = {}
    return JsonResponse(data)

def studentDownload(request):
    id = []
    family = []
    name = []
    fName = []
    studentClass = []
    username = []
    stdFees = []
    stdMonth = []
    contact = []
    address = []
    admissionDate = []

    students = Students.objects.filter(status="Active")
    fees = StudentFees.objects.all()
    def_students = {}
    month = []

    for student in students:
        id.append("EE"+str(student.user.id))
        family.append("ED-"+str(student.family))
        name.append(student.user.first_name)
        fName.append(student.fname)
        studentClass.append(student.studentClass)
        username.append(student.user.username)
        stdFees.append(student.fees)
        contact.append(student.contact)
        address.append(student.address)
        admissionDate.append(student.admissionDate)
        for fee in fees:
            if fee.feeMonth not in month:
                month.append(fee.feeMonth)
            if student.user.id == fee.students.user.id:
                if ("EE"+str(student.user.id)) in def_students:
                    def_students["EE"+str(student.user.id)][fee.feeMonth] = fee.feeStatus
                else:
                    def_students["EE"+str(student.user.id)] = {
                        fee.feeMonth:fee.feeStatus 
                    }
    print(def_students)
    month.reverse()
    month1 = []
    for i in range(12):
        try:
            month1.append(month[i])
        except:
            break

    
    for key in def_students:
        for mon in month1:
            if mon not in def_students[key]:
                def_students[key][mon] = "None"


    data = {
        "Id": id, 
        "Family#":family, 
        "Name":name, 
        "F.Name":fName, 
        "Class":studentClass, 
        "Username":username, 
        "Contact#":contact, 
        "Address":address, 
        "Admission":admissionDate
        }

    for m in month:
        data2 = []
        for i in id:
            print(i)
            data2.append(def_students[i][m])
        data[m] = data2
    
        
    df = pd.DataFrame(data)
    df.to_csv(r'./media/students.csv', sep=',',index=False)
    
    data = {}
    return JsonResponse(data)

