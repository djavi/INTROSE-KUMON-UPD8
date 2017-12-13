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

from kumon.forms import LoginForm, StudentForm, TeacherForm, ScheduleForm, EditTeacherForm, EditStudentForm

from .models import User, Student, Teacher, Schedule, Expenses, Item, sTime, Tuition, savedTuition,totalTuition,Salary,addEntry,delEntry

def create_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        kind = request.POST.get("kind")
        user = User(username=username,password=password,level=kind,amount=0)
        user.save()
        return redirect('home')

    return render(request,"kumon/index.html",{})

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
                    request.session['user'] = i.id
                    return redirect('home')
        error = "Invalid username/password"

        return render(request,'kumon/login.html',{'error':error,'form':form})
    context = {
        'all_users': all_users,
        'form':form,
    }

    return render(request, 'kumon/login.html', context)	

def logout(request):
    del request.session['user']
    return redirect('login')

def home(request):
    user = User.objects.get(pk=request.session['user'])
    context = {
        'user':user,
    }
    return render(request,'kumon/index3.html',context)

def studentPage(request):
    user = User.objects.get(pk=request.session['user'])
    
    all_students = Student.objects.all()
    
    if request.method == "GET":
        if "search" in request.GET:
            searched = request.GET.get('search')
            all_students = Student.objects.filter(nickname__contains=searched) | Student.objects.filter(firstname__contains=searched) | Student.objects.filter(lastname__contains=searched) | Student.objects.filter(middlename__contains=searched)
	
    filter = 'firstname'
    if request.POST.get('sort'):
        filter = request.POST.get('sort')
	
    all_students = all_students.order_by(filter)
    
    context = {
        'all_students':all_students,
        'user':user,
    }
    return render(request,'kumon/students.html',context)

def studentProfile(request, student_id):
    user = User.objects.get(pk=request.session['user'])
    all_students = Student.objects.all()

    try:
        student = Student.objects.get(pk=student_id)
    except (KeyError, Student.DoesNotExist):
        raise Http404("Student does not exist")
	
	
    if request.POST.get('Delete'):
        student.delete()
        return redirect('students')
		
    context = {
        'all_students':all_students,
        'student':student,
        'user':user,
    }
    return render(request,'kumon/student-profile.html',context)


def addStudent(request):
	form = StudentForm(request.POST or None, request.FILES or None)
	all_students = Student.objects.all()

	if form.is_valid():
		student = form.save(commit=False)
		today = datetime.date.today()
		student.age = today.year - student.birthdate.year - ((today.month, today.day) < (student.birthdate.month, student.birthdate.day))
		student.save()
		return redirect('students')
        
	return render(request, 'kumon/add-student.html', {'form':form})
	
def editStudent(request, student_id):
	form = EditStudentForm(request.POST or None, request.FILES or None)
	all_students = Student.objects.all()
	student = Student.objects.get(pk=student_id)
	
	if form.is_valid():
		student = form.save(commit=False)
		student.save()
		
	return render(request, 'kumon/edit-student.html', {'form':form, 'student':student})	
	
def editTeacher(request, teacher_id):
	form = EditTeacherForm(request.POST or None, request.FILES or None)
	all_teachers = Teacher.objects.all()
	teacher = Teacher.objects.get(pk=teacher_id)
	
	if form.is_valid():
		teacher = form.save(commit=False)
		teacher.save()
		
	return render(request, 'kumon/edit-teacher.html', {'form':form, 'teacher':teacher})	


def addTeacher(request):
    form = TeacherForm(request.POST or None, request.FILES or None)
    all_teachers = Teacher.objects.all()

    if form.is_valid():
        teacher = form.save(commit=False)
        teacher.save()
        salary = Salary(teacher=teacher,salary=0,total=0)
        salary.save()
        #return render(request, 'kumon/teachers.html', {'all_teachers':all_teachers})
        return redirect('teacher')

    return render(request, 'kumon/add-teacher.html', {'form':form})

def teacherPage(request):
    user = User.objects.get(pk=request.session['user'])
    all_teachers = Teacher.objects.all()
    context = {
        'all_teachers':all_teachers,
        'user':user
    }
    
    return render(request,'kumon/teachers.html',context)

def teacherProfile(request, teacher_id):
    #all_teachers = Teachers.objects.all()
    user = User.objects.get(pk=request.session['user'])
    try:
        teacher = Teacher.objects.get(pk=teacher_id)
        all_schedules = Schedule.objects.filter(teacher=teacher)
    except (KeyError, Teacher.DoesNotExist):
        raise Http404("Teacher does not exist")

    if request.POST.get('Delete'):
        teacher.delete()
        return redirect('teachers')

    context = {
        #'all_teachers':all_teachers,
        'teacher':teacher,
        'all_schedules':all_schedules,
        'user':user,
    }
    return render(request,'kumon/profile.html',context)
    

def attendancePage(request):
    all_students = Student.objects.all()
    user = User.objects.get(pk=request.session['user'])
    all_sTime = sTime.objects.all()
    a = datetime.datetime.now().date()
    a = a.strftime('%Y-%m-%d')
    studentList = []
    if request.method == "GET":
        if "date" in request.GET:
            a = request.GET.get("date")
            
    month = a[5:-3]
    year = a[:-6]
    day = a[8:]

    ids = sTime.objects.all().values_list('student',flat=True)

    for student in ids:
        studentList.append([Student.objects.get(pk=student)])
        
    print(studentList)
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
        'user':user
    }
    return render(request,'kumon/Attendance.html',context)


def paymentPage(request):
    all_students = Student.objects.all()
    all_tuition = Tuition.objects.all()
    all_saved = savedTuition.objects.all()
    all_total = totalTuition.objects.all()            
    now = str(datetime.datetime.now().date())
    a = datetime.datetime.now().date()
    a = a.strftime('%Y-%m-%d')
    error = None
    to_update =[]

    nMonth = now[5:-3]
    nYear = now[:-6]
    nDay = now[8:]
    n0w = (nYear + '-' + nMonth)

    month = a[5:-3]
    year = a[:-6]
    a = (year + '-' + month)
    choice = None

    if request.method == "GET":
        if "date" in request.GET:
            a = request.GET.get("date")
            year = a[:4]
            month = a[5:]
            print(a)
            print(n0w)

    if request.method == "GET":
        if "list" in request.GET:
            choice = request.GET.get("list")
            all_students = all_students.filter(tuition__paid=choice)

    if request.method == "POST":
        if "add" in request.POST:
            print("ADD")
            for a in request.POST:
                print(a)
            #studentId = int(request.POST.get("studentId"))
            #print(request.POST.get("studentId"))
            student = request.POST.get("studList")
            ornum = request.POST.get("or-number")
            date = request.POST.get("date")
            payment = request.POST.get("payment")
            
            for a in all_tuition:
                if(ornum == a.OR_number):
                    error = "Same OR number"
                    context = {
                    'all_students':all_students,
                    'all_tuition':all_tuition,
                    'a':a,
                    'n0w':n0w,
                    'error':error
                    }
                    return render(request,'kumon/payment.html',context)

            tuition = Tuition.objects.get(name__exact=student)
            tuition.OR_number = ornum
            tuition.date = date
            tuition.payment = payment
            tuition.paid = 'Fully Paid'
            tuition.save()
            
            return redirect('payments')
            if(month == date[5:-3] and year == date[:-6]):
                total = totalTuition(student=all_students.get(name__exact=student),totalPaid='0',needPay='5000',)

            
    if request.method == "POST":
        if "update" in request.POST:
            print("Update")
            print("level " + request.POST.get("level"))
            print("paid " + request.POST.get("pay"))
            level = request.POST.get("level")
            pay = request.POST.get("pay")

            if level == 'Grade 6 and below':
                a = savedTuition.objects.get(pk=1)
                a.date = datetime.datetime.now().date()
                a.below_g6 = pay
                a.above_g7 = a.above_g7
                a.save()
            elif level == 'Grade 7 and above':
                a = savedTuition.objects.get(pk=1)
                a.date = datetime.datetime.now().date()
                a.below_g6 = a.below_g6
                a.above_g7 = pay
                a.save()

    if request.method == "GET":
        if "q" in request.GET:
            all_students = all_students.filter(firstname__contains=request.GET.get("q")) | all_students.filter(lastname__contains=request.GET.get("q"))
    
    if request.method == "POST":
        if "remove" in request.POST:
            for old_items in request.POST:
                print(old_items)
                print(old_items[:4])
                if old_items[:4] == "del-":
                    to_update.append([old_items[4:],request.POST.get(old_items)])
        print(to_update)
        for expense in to_update:
            if expense[1] == 'on':
                b = Tuition.objects.get(pk=expense[0])
                print(b.date)
                b.date = None
                b.OR_number = None
                b.payment = None
                b.paid = "Not Yet Paid"
                b.save()

        return redirect('payments')

    bbb = savedTuition.objects.get(pk=1)
    context = {
        'all_students':all_students,
        'all_tuition':all_tuition,
        'a':a,
        'n0w':n0w,
        'error':error,
        'bbb':bbb,
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


def schedulePage(request):
    all_students = Student.objects.all()
    all_schedules = Schedule.objects.all()
    form = ScheduleForm(request.POST)
    to_update = []

    if request.method == "POST":
        if "update" in request.POST:
            form = ScheduleForm(request.POST)
            print(form['teacher'].value())
            print(form.data['teacher'])
            for items in request.POST:
                print(items)
                print(items[:4])
                if items[:4] == "add-":
                    to_update.append([items[4:],request.POST.get(items)])
            
            print(to_update)

            for sched in to_update:
                if sched[1] == 'on':
                    stud = Student.objects.get(pk=sched[0])
                    teacher = form['teacher'].value()
                    day = form['day'].value()
                    timeslots = form['timeslots'].value()
                    final = Schedule(teacher=Teacher.objects.get(pk=teacher),student=stud,day=day,timeslots=timeslots)
                    final.save()
        
        elif "remove" in request.POST:
            form = ScheduleForm(request.POST)
            for items in request.POST:
                if items[:4] == "add-":
                    to_update.append([items[4:],request.POST.get(items)])
                
            for sched in to_update:
                if sched[1] == 'on':
                    stud = Student.objects.get(pk=sched[0])
                    teacher = form['teacher'].value()
                    day = form['day'].value()
                    timeslots = form['timeslots'].value()

                    final = Schedule.objects.filter(student=stud).filter(teacher__id=teacher).filter(day=day).filter(timeslots=timeslots)
                    final.delete()

    context = {
        'all_students':all_students,
        'all_schedules':all_schedules,
        'form':form,
    }

    return render(request,'kumon/Schedule.html',context)

def salaryFormatPage(request):
    all_teachers = Teacher.objects.all()
    all_add = addEntry.objects.all()
    all_del = delEntry.objects.all()
    length = len(all_add) + 1
    length2 = len(all_del) + 1
    to_update = []
    to_update2 = []
    all_salary = Salary.objects.all()
    all_users = User.objects.all()
    user = User.objects.get(pk=1)

    if request.method == "POST":
        if "add" in request.POST:
            choice = request.POST.get("type")
            name = request.POST.get("sal_option")
            value = request.POST.get("value")
            print(choice)
            if choice == "Additional":
                add = addEntry(name=name,value=value)
                add.save()
                return redirect('salary_format')
            elif choice == "Deduction":
                deduc = delEntry(name=name,value=value)
                deduc.save()
                return redirect('salary_format')

    if request.method == "POST":
        if "submit" in request.POST:
            allowance = request.POST.get("allowance_amount")
            print(allowance)
            user.amount = float(allowance)
            user.save()
            print(user.amount)
            for old_items in request.POST:
                print(old_items)
                print(old_items[:4])
                if old_items[:4] == "add-":
                    to_update.append([old_items[4:], float(request.POST.get(old_items))])

            print(to_update)

            for item in to_update:
                item_obj = addEntry.objects.get(pk=item[0])
                item_obj.value = item[1]
                item_obj.save()


            for old_items in request.POST:
                print(old_items[:4])
                if old_items[:4] == "del-":
                    to_update2.append([old_items[4:], float(request.POST.get(old_items))])

            print(to_update2)

            for item in to_update2:
                item_obj = delEntry.objects.get(pk=item[0])
                item_obj.value = item[1]
                item_obj.save()
            
            for teacher in all_teachers:
                for salary in all_salary:
                    if salary.teacher == teacher:
                        salary.teacher = teacher
                        salary.salary = allowance
                        
                        salary.save()
            
            return redirect('salary')

    if request.method == "POST":
        if "remove" in request.POST:
            for old_items in request.POST:
                print(old_items)
                print(old_items[:15])
                if old_items[:15] == "item_check_del-":
                    to_update2.append([old_items[15:], request.POST.get(old_items)])
                elif old_items[:15] == "item_check_add-":
                    to_update.append([old_items[15:],request.POST.get(old_items)])

        for expense in to_update2:
            if expense[1] == 'on':
                delEntry.objects.get(pk=expense[0]).delete()
        
        for expense in to_update:
            if expense[1] == 'on':
                addEntry.objects.get(pk=expense[0]).delete()
        
        return redirect('salary_format')

    context = {
        'all_add':all_add,
        'length':length,
        'length2':length2,
        'all_del':all_del,
        'user': user,
    }

    return render(request, 'kumon/salaries_format.html',context)

def salaryFormatUpdate(request):

    return render(request, 'kumon/salaries_format.html',context)

def teacherSalaryPage(request,id):
    teacher = Teacher.objects.get(pk=id)
    all_add = addEntry.objects.all()
    all_del = delEntry.objects.all()
    salary = Salary.objects.get(teacher=teacher)
    length = len(all_add) + 1
    length2 = len(all_del) + 1

    context = {
        'salary':salary,
        'all_add':all_add,
        'all_del':all_del,
        'length':length,
        'length2':length2,
    }

    return render(request,'kumon/teacher_salary.html',context)

def get(request,id):
    teacher = Teacher.objects.get(pk=id)
    all_add = addEntry.objects.all()
    all_del = delEntry.objects.all()
    salary = Salary.objects.get(teacher=teacher)
    length = len(all_add) + 1
    length2 = len(all_del) + 1

    data = {
        'salary':salary,
        'all_add':all_add,
        'all_del':all_del,
        'length':length,
        'length2':length2,
    }
    
    #pdf = render_to_pdf('kumon/teacher_salary.html', data)
    #return HttpResponse(pdf, content_type='application/pdf')

def salaryPage(request):
    all_teachers = Teacher.objects.all()

    context = {'all_teachers':all_teachers,}

    return render(request,'kumon/salaries.html',context)