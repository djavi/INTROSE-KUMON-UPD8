from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView
from django.shortcuts import redirect,reverse
from django.urls import reverse

import datetime

# Create your views here.

from kumon.forms import LoginForm, StudentForm, TeacherForm, ScheduleForm

from .models import User, Student, Teacher, Schedule, Expenses, Item, sTime

def login(request):
    form = LoginForm(request.POST)
    all_users = User.objects.all()
    error = ''

    if form.is_valid():
        lUser = form.cleaned_data['username']
        lPass = form.cleaned_data['password']

        for i in all_users:
            if i.username == lUser:
                if i.password == lPass: 
                    return redirect('home')
        error = "Invalid username/password"

        return render(request,'kumon/login.html',{'error':error,'form':form})
    context = {
        'all_users': all_users,
        'form':form,
    }

    return render(request, 'kumon/login.html', context)	


def home(request):

    context = {
    }
    return render(request,'kumon/index3.html',context)

def studentPage(request):
    all_students = Student.objects.all()
    context = {
        'all_students':all_students,
    }
    return render(request,'kumon/students.html',context)

def studentProfile(request, student_id):
    all_students = Student.objects.all()

    try:
        student = Student.objects.get(pk=student_id)
    except (KeyError, Student.DoesNotExist):
        raise Http404("Student does not exist")

    context = {
        'all_students':all_students,
        'student':student,
    }
    return render(request,'kumon/student-profile.html',context)


def addStudent(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    all_students = Student.objects.all()

    if form.is_valid():
        student = form.save(commit=False)
        student.save()
        #return render(request, 'kumon/students.html', {'all_students':all_students})
        return redirect('students')

    return render(request, 'kumon/add-student.html', {'form':form})

def addTeacher(request):
    form = TeacherForm(request.POST or None, request.FILES or None)
    all_teachers = Teacher.objects.all()

    if form.is_valid():
        teacher = form.save(commit=False)
        teacher.save()
        #return render(request, 'kumon/teachers.html', {'all_teachers':all_teachers})
        return redirect('teacher')

    return render(request, 'kumon/add-teacher.html', {'form':form})

def teacherPage(request):
    all_teachers = Teacher.objects.all()
    context = {
        'all_teachers':all_teachers,
    }
    
    return render(request,'kumon/teachers.html',context)

def teacherProfile(request, teacher_id):
    #all_teachers = Teachers.objects.all()

    try:
        teacher = Teacher.objects.get(pk=teacher_id)
    except (KeyError, Teacher.DoesNotExist):
        raise Http404("Teacher does not exist")

    context = {
        #'all_teachers':all_teachers,
        'teacher':teacher,
    }
    return render(request,'kumon/profile.html',context)
    

def attendancePage(request):
    all_students = Student.objects.all()
    all_sTime = sTime.objects.all()
    a = datetime.datetime.now().date()
    a = a.strftime('%Y-%m-%d')
    if request.method == "GET":
        if "date" in request.GET:
            a = request.GET.get("date")
            
    month = a[5:-3]
    year = a[:-6]
    day = a[8:]
 

    if request.method == "POST":
        if request.POST.get("attend") and request.POST.get("student"):
            print(request.POST.get("attend"))
            print(request.POST.get("student"))
    
    now = datetime.datetime.now().date()
    all_sTime = sTime.objects.filter(day__year=year,day__month=month,day__day=day)
   
    context = {
        'all_students':all_students,
        'all_sTime':all_sTime,
        'a':a,
        'now':now,
    }
    return render(request,'kumon/Attendance.html',context)

def salaryPage(request):
    all_teachers = Teacher.objects.all()

    context = {'all_teachers':all_teachers,}

    return render(request,'kumon/salaries.html',context)

def paymentPage(request):
    all_students = Student.objects.all()
    to_update = []

    if "add" in request.POST:
        for old_items in request.POST:
            print(old_items)
            if "item-" in old_items:
                to_update.append([old_items[5:], int(request.POST.get(old_items))])

        print(to_update)
    '''
        for stud in to_update:
            stud_obj = Student.objects.get(student=student[0])
            stud_obj.stock = stud_obj.stock + student[1]

            stud_obj.save()

        for item in to_update:
            item_obj = Item.objects.get(item=item[0])
            item_obj.stock = item_obj.stock + item[1]
            
    '''

    if request.method == "GET":
        if "q" in request.GET:
            all_students = all_students.filter(name__contains=request.GET.get("q"))

    context = {
        'all_students':all_students,
    }

    return render(request,'kumon/payment.html',context)


def paymentUpdate(request):
    all_students = Student.objects.all()
    to_update = []

    context = {
        'all_students':all_students,
    }

    return render(request,'kumon/payment.html',context)


def expensesPage(request):
    context = {}
    expenses = Expenses.objects.all()
    expenses = Expenses.objects.order_by('added').reverse()

    a = datetime.datetime.now().date()
    a = a.strftime('%Y-%m-%d')
            
    now = str(datetime.datetime.now().date())
    
    nMonth = now[5:-3]
    nYear = now[:-6]
    n0w = (nYear + '-' + nMonth)

    month = a[5:-3]
    year = a[:-6]
    a = (year + '-' + month)
    expenses = Expenses.objects.filter(added__year__exact=year,
                                    added__month__exact=month)

    if request.GET.get('q'):
        expenses = Expenses.objects.filter(added=request.GET.get('q'))

    if request.method == "GET":
        if "date" in request.GET:
            a = request.GET.get("date")
            year = a[:4]
            month = a[5:]
            expenses = Expenses.objects.filter(added__year__exact=year,
                                              added__month__exact=month)
            print(a)

    
    print(a)
    context = {
        "expenses": expenses,
        "a":a,
        "n0w":n0w
    }

    return render(request,'kumon/expenses.html',context)

def inventoryPage(request):
    context = {}
    items = Item.objects.all()
    items = Item.objects.order_by('item')

    if request.method == "GET":
        if "q" in request.GET:
            items = items.filter(item__icontains=request.GET.get("q"))

    context = {
        "items": items
    }

    return render(request, 'kumon/inventory.html',context)

def inventoryAdd(request):
    context = {}
    items = Item.objects.all()
    items = Item.objects.order_by('item')
    error = None

    if request.method == "POST":
        if request.POST.get("item") and request.POST.get("stock"):
            item = Item.objects.filter(item=request.POST.get("item"))

            if item.count() <= 0:
                try:
                    if int(request.POST.get("stock")) >= 0:
                        item = Item(item=request.POST.get("item"), stock=int(request.POST.get("stock")))
                        item.save()
                    else:
                        error = "The item cost must be positive or zero."
                except ValueError:
                    error = "The stock ammount entered is invalid."
            else:
                error = "The item name must be unique."
        else:
            error = "The item name or the item cost is missing."

    context = {
        "items": items,
        "error": error,
    }

    return render(request, 'kumon/inventory.html',context)

def inventoryUpdate (request):
    context = {}
    items = Item.objects.all()
    items = Item.objects.order_by('item')
    to_update = []

    if "add" in request.POST:
        for old_items in request.POST:
            if old_items[:5] == "item-":
                print(old_items)
                to_update.append([old_items[5:], int(request.POST.get(old_items))])

        for item in to_update:
            item_obj = Item.objects.get(item=item[0])
            item_obj.stock = item_obj.stock + item[1]

            if item_obj.stock < 0:
                item_obj.stock = 0

            item_obj.save()

    elif "subtract" in request.POST:
        for old_items in request.POST:
            if old_items[:5] == "item-":
                to_update.append([old_items[5:], int(request.POST.get(old_items))])

        for item in to_update:
            item_obj = Item.objects.get(item=item[0])
            item_obj.stock = item_obj.stock - item[1]

            if item_obj.stock < 0:
                item_obj.stock = 0

            item_obj.save()
    elif "remove" in request.POST:
        for old_items in request.POST:
            if old_items[:11] == "item_check-":
                to_update.append([old_items[11:], request.POST.get(old_items)])

        for item in to_update:
            if item[1] == 'on':
                Item.objects.get(item=item[0]).delete()

    context["items"] = items
    return render(request, 'kumon/inventory.html', context)

def expensesUpdate(request):
    context = {}
    to_update = []
    expenses = Expenses.objects.all()
    expenses = Expenses.objects.order_by('added').reverse()


    a = datetime.datetime.now().date()
    a = a.strftime('%Y-%m-%d')
            
    now = str(datetime.datetime.now().date())
    
    nMonth = now[5:-3]
    nYear = now[:-6]
    n0w = (nYear + '-' + nMonth)

    month = a[5:-3]
    year = a[:-6]
    a = (year + '-' + month)
    expenses = Expenses.objects.filter(added__year__exact=year,
                                    added__month__exact=month)


    if "save" in request.POST:
        for old_expenses in request.POST:
            if old_expenses[:14] == "expense_check-":
                to_update.append(old_expenses[14:])

        for expense in Expenses.objects.all():
            if expense.item in to_update:
                expense.paid = True
            else:
                expense.paid = False

            expense.save()


    elif "remove" in request.POST:
        for old_expenses in request.POST:
            if old_expenses[:18] == "rem_expense_check-":
                to_update.append([old_expenses[18:], request.POST.get(old_expenses)])

        for expense in to_update:
            if expense[1] == 'on':
                Expenses.objects.get(item=expense[0]).delete()

    context = {
        "expenses": expenses,
        "a":a,
        "n0w":n0w
    }
    return render(request, 'kumon/expenses.html', context)

def exspensesAdd(request):
    context = {}
    error = None
    expenses = Expenses.objects.all()
    expenses = Expenses.objects.order_by('added').reverse()

    a = datetime.datetime.now().date()
    a = a.strftime('%Y-%m-%d')
            
    now = str(datetime.datetime.now().date())
    
    nMonth = now[5:-3]
    nYear = now[:-6]
    n0w = (nYear + '-' + nMonth)

    month = a[5:-3]
    year = a[:-6]
    a = (year + '-' + month)
    expenses = Expenses.objects.filter(added__year__exact=year,
                                    added__month__exact=month)



    if request.POST.get('item') and request.POST.get('cost') and request.POST.get('date'):
        expense = Expenses.objects.filter(item=request.POST.get('item'))

        if expense.count() <= 0:
            try:
                if int(request.POST.get('cost')) >= 0:
                    try:
                        datetime.datetime.strptime(request.POST.get('date'), "%Y-%m-%d")
                        
                        expense = Expenses(item=request.POST.get('item'), cost=int(request.POST.get('cost')), added=request.POST.get('date'), paid=True if "paid" in request.POST else False)
                        expense.save()
                    except ValueError:
                        error = "The added date is in an invalid format."
                else:
                    error = "The expense cost must be positive or greater than zero."
            except ValueError:
                error = "The expense cost entered is invalid."
        else:
            error = "The expense title must be unique."
    else:
        error = "The expense title, cost, or added date is missing."

    context = {
        "expenses": expenses,
        "a":a,
        "n0w":n0w,
        "error":error
    }
    if(error != None):
        return render(request, 'kumon/expenses.html', context)
    else:
        return redirect('expenses')

def salaryFormatPage(request):
    context = {

    }

    return render(request, 'kumon/salaries_format.html',context)

def teacherSalaryPage(request):
    context = {
        
    }

    return render(request,'kumon/teacher_salary.html',context)


def schedulePage(request):
    all_students = Student.objects.all()
    all_schedules = Schedule.objects.all()
    form = ScheduleForm(request.GET)

    context = {
        'all_students':all_students,
        'all_schedules':all_schedules,
        'form':form,
    }

    return render(request,'kumon/Schedule.html',context)