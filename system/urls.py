from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('home', views.home, name="home"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('students', views.students, name="students"),
    path('teachers', views.teachers, name="teachers"),
    path('incharge', views.incharge, name="incharge"),
    path('classes', views.classes, name="classes"),
    path('subjects', views.subjects, name="subjects"),
    path('fees', views.fees, name="fees"),
    path('fee-receipt', views.feeReceipt, name="feeReceipt"),
    path('fee-receipt-value', views.feeReceiptValue, name="feeReceiptValue"),
    path('attendence', views.attendence, name="attendence"),
    path('add-attendence', views.addAttendence, name="addAttendence"),
    path('change-attendence', views.changeAttendence, name="changeAttendence"),
    path('income', views.income, name="income"),
    path('expense', views.expense, name="expense"),
    path('reports', views.reports, name="reports"),
    path('register-student', views.registerStudents, name="registerStudents"),
    path('register-teacher', views.registerTeacher, name="registerTeacher"),
    path('update-student', views.updateStudents, name="updateStudents"),
    path('update-teacher', views.updateTeacher, name="updateTeacher"),
    path('delete-student', views.deleteStudents, name="deleteStudents"),
    path('delete-fee', views.deleteFee, name="deleteFee"),
    path('delete-teacher', views.deleteTeacher, name="deleteTeacher"),
    path('settings', views.settings, name="settings"),
    path('check-family', views.checkFamily, name='checkFamily'),
    path('clear-exp', views.clearExp, name='clearExp'),
    path('clear-inc', views.clearInc, name='clearInc'),
    path('clear-balance', views.clearBalance, name='clearBalance'),
    path('itoc', views.itoc, name='itoc'),
    path('subject-delete', views.subjectDelete, name='subjectDelete'),
    path('class-delete', views.classDelete, name='classDelete'),
    path('std-delete', views.stdDelete, name='stdDelete'),
    path('fee-delete', views.feeDelete, name='feeDelete'),
    path('inc-delete', views.incDelete, name='incDelete'),
    path('exp-delete', views.expDelete, name='expDelete'),
    path('tec-delete', views.tecDelete, name='tecDelete'),
    path('std-update', views.stdUpdate, name='stdUpdate'),
    path('tec-update', views.tecUpdate, name='tecUpdate'),
    path('upload-header', views.uploadHeader, name='uploadHeader'),
    path('student-dashboard', views.studentDashboard, name='studentDashboard'),
    path('month-data', views.monthData, name='monthData'),
    path('username-check', views.usernameCheck, name='usernameCheck'),
    path('get-family', views.getFamily, name='getFamily'),
    path('contact-download', views.contactDownload, name='contactDownload'),
    path('income-download', views.incomeDownload, name='incomeDownload'),
    path('expense-download', views.expenseDownload, name='expenseDownload'),
    path('student-download', views.studentDownload, name='studentDownload'),
    path('student-feePaid-download', views.studentFeePaidDownload, name='studentFeePaidDownload'),
    path('documents', views.documents, name='documents'),
    path('del-documents', views.delDocuments, name='delDocuments'),
    path('del-marks', views.delMarks, name='delMarks'),
    path('import-csv', views.importCSV, name='importCSV'),
    path('send-sms', views.sendSMS, name='sendSMS'),
    path('send-sms-all', views.sendSMSAll, name='sendSMSAll'),
]
