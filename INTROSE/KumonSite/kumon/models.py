from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator

# Create your models here.


class User(models.Model):
    choices = (
        ('Admin', 'Admin'),
        ('Teacher', 'Teacher'),
    )
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=50)
    level = models.CharField(max_length=20, choices=choices, default='Admin')
    amount = models.DecimalField(blank=True,max_digits=7,decimal_places=2)

    def __str__(self):
        return self.username
    
class Teacher(models.Model):
	
	gender_choices = (
		('Male','Male'),
		('Female','Female')
	)
	
	#name = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	firstname = models.CharField(max_length=50)
	middlename = models.CharField(max_length=50)
	birthdate = models.DateField(auto_now=False)
	age = models.IntegerField()	
	gender = models.CharField(
		max_length=10,
		choices = gender_choices,
		default = 'Male'
	)
	address = models.CharField(max_length=100)
	phone_num = models.CharField(max_length=15)
	tel_num = models.CharField(max_length=15)
	email = models.EmailField(max_length=50)
	t_picture = models.ImageField(blank=True,default='profile_img/image.png',upload_to="profile_img")

	
	subject_choice = (
		('Reading','Reading'),
		('Math','Math'),
		('Reading and Math','Reading and Math')
		)
	subject = models.CharField(choices=subject_choice, max_length=20)
	
	def __str__(self):
		return self.firstname

class Student(models.Model):
	gender_choices = (
		('Male','Male'),
		('Female','Female')
	)
	#Basic Details
	#name = models.CharField(max_length=59)
	lastname = models.CharField(max_length=50)
	firstname = models.CharField(max_length=50)
	middlename = models.CharField(max_length=50)
	nickname = models.CharField(max_length=25)
	birthdate = models.DateField(auto_now=False)
	age = models.IntegerField()	
	gender = models.CharField(
		max_length=10,
		choices = gender_choices,
		default = 'Male'
	)
	picture = models.ImageField(blank=True, default='profile_img/image.png',upload_to="profile_img")

	#Contact Info
	phone_num = models.IntegerField(max_length=11)
	tel_num = models.IntegerField(max_length=7)
	address = models.CharField(max_length=100)
	email = models.EmailField(max_length=50)
	student_num = models.IntegerField()

	kumon_level_choices = (
		('PK3','PK3'),('PK2','PK2'),('PK1','PK1'),('K','K'),('Grade 1',' Grade 1'),
		('Grade 2',' Grade 2'),('Grade 3',' Grade 3'),('Grade 4',' Grade 4'),('Grade 5',' Grade 5'),
		('Grade 6',' Grade 6'),('Grade 7',' Grade 7'),('Grade 8',' Grade 8'),('Grade 8',' Grade 8'),
		('Grade 9',' Grade 9'),('Grade 10',' Grade 10'),('Grade 11',' Grade 11'),('Grade 12',' Grade 12'),
		('Grade 13',' Grade 13'),
	)

	kumon_levelM_choices = (
		('9A','9A'),('8A','8A'),('7A','7A'),('6A','6A'),('5A','5A'),
		('4A','4A'),('3A','3A'),('2A','2A'),('A','A'),('B','B'),
		('C','C'),('D','D'),('E','E'),('F','F'),('G','G'),
		('H','H'),('I','I'),('J','J'),('K','K'),('L','L'),
		('M','M'),('N','N'),('O','O'),('X','X'),
	)
	
	kumon_levelR_choices = (
		('7A','7A'),('6A','6A'),('5A','5A'),
		('4A','4A'),('3A','3A'),('2A','2A'),
		('AI','AI'),('AII','AII'),('BI','BI'),('BI','BII'),
		('CI','CI'),('CII','CII'),('DI','DI'),('DI','DII'),
		('EI','EI'),('EII','EII'),('FI','FI'),('FI','FII'),
		('GI','GI'),('GII','GII'),('HI','HI'),('HI','HII'),
		('II','II'),('III','III'),('J','J'),('K','K'),('L','L'),
	)

	#Other Info
	school = models.CharField(max_length=50)
	school_level = models.CharField(max_length=50, choices = kumon_level_choices,default = 'PK3')
	date_enrolled = models.DateField(auto_now=False)
	kumon_levelM = models.CharField(max_length=50, choices = kumon_levelM_choices, default = '9A')
	kumon_levelR = models.CharField(max_length=50, choices = kumon_levelR_choices, default = '7A')

	rank_choices = (
		('Bronze','Bronze'),
		('Silver','Silver'),
		('Gold','Gold'),
		('None','None')
		)

	ashrR = models.CharField(
		max_length=10,
		choices = rank_choices,
		default = 'None'
	) #Gold, Silver, Bronze 

	ashrM = models.CharField(
		max_length=10,
		choices = rank_choices,
		default = 'None'
	) #Gold, Silver, Bronze 
		
	
	#Guardian Info 
	guardian_name = models.CharField(max_length=50)
	relation = models.CharField(max_length=50)
	guardian_num = models.IntegerField(max_length=11) #Phone / Tel
	guardian_email = models.EmailField(max_length=50,blank=True)

        #teacher/s will be found in schedule

	#sched = models.ForeignKey(Schedule, on_delete=models.CASCADE)

	#Status
	status_choices = (
                ('Active','active'),
                ('NonActive','nonactive'),
				('Completed', 'completed')
        )
	
	status = models.CharField(
                max_length=10,
                choices = status_choices,
                default = 'Active'
        )
		         
	def __str__(self):
		return self.firstname

class Tuition(models.Model):  #connect to student
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    choice = (
        ('Fully Paid', 'Fully Paid'),
        ('Partially Paid', 'Partially Paid'),
        ('Not Yet Paid', 'Not Yet Paid'),
    )

    OR_number = models.CharField(max_length=100,blank=True,null=True)
    date = models.DateField(auto_now=False,blank=True,null=True)
    payment = models.DecimalField(decimal_places=2,max_digits=7,blank=True,null=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):  #delete

    days_week = (('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
                 ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                 ('Friday', 'Friday'), ('Saturday', 'Saturday'))

    time_slots = (
        ('10to11', '10:00am - 11:00am'),
        ('11to12', '11:00am - 12:00pm'),
        ('12to1', '12:00pm - 1:00pm'),
        ('1to2', '1:00pm - 2:00pm'),
        ('2to3', '2:00pm - 3:00pm'),
        ('3to4', '3:00pm - 4:00pm'),
        ('4to5', '4:00pm - 5:00pm'),
        ('5to6', '5:00pm - 6:00pm'),
        ('6to7', '6:00pm - 7:00pm'),
    )

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    timeslots = models.CharField(
        max_length=50,
        choices=time_slots,
        default='10to11',
    )
    day = models.CharField(max_length=10, choices=days_week, default='Monday')

    def __str__(self):
        return self.timeslots


class Expenses(models.Model):
    item = models.CharField(max_length=50, unique=True)
    cost = models.DecimalField(decimal_places=2,max_digits=7)
    added = models.DateField()

    paid = models.BooleanField(blank=True)

    def __str__(self):
        return self.item


class Item(models.Model):
    item = models.CharField(max_length=50, unique=True)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.item


class sTime(models.Model):  #connect to student
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    day = models.DateField(auto_now=False)
    sAbsent = models.BooleanField()

    def __str__(self):
        return self.student.firstname


class tTime(models.Model):  #connect to teacher
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    tAbsent = models.BooleanField()
    timeIn = models.TimeField()
    timeOut = models.TimeField()


class savedTuition(models.Model):
    below_g6 = models.FloatField()
    above_g7 = models.FloatField()
    date = models.DateField()


class Salary(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    salary = models.DecimalField(decimal_places=2,max_digits=7)
    total = models.DecimalField(decimal_places=2,max_digits=7)

    def __str__(self):
        return(self.teacher.firstname)

class addEntry(models.Model):
    name = models.CharField(max_length=50)
    value = models.DecimalField(decimal_places=2,max_digits=7)

    def __str__(self):
        return (self.name)

class delEntry(models.Model):
    name = models.CharField(max_length=50)
    value = models.DecimalField(decimal_places=2,max_digits=7)

    def __str__(self):
        return (self.name)

class tAddEntry(models.Model):
	teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	value = models.DecimalField(decimal_places=2,max_digits=7)

class tDelEntry(models.Model):
	teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	value = models.DecimalField(decimal_places=2,max_digits=7)

class Grades(models.Model):
	#student = models.ForeignKey(Student, on_delete=models.CASCADE)
	subject_choice = (
		('Math', 'math'), ('Reading', 'reading')
	)
	subject = models.CharField(choices=subject_choice, max_length=10)
	
	test_choice = (
		('Achievement', 'achievement'),
		('Diagnostic', 'diagnostic')
	)
	test = models.CharField(max_length=15, choices = test_choice)
	
	level_choices = (
		('PK3','PK3'),('PK2','PK2'),('PK1','PK1'),('K','K'),('Grade 1',' Grade 1'),
		('Grade 2',' Grade 2'),('Grade 3',' Grade 3'),('Grade 4',' Grade 4'),('Grade 5',' Grade 5'),
		('Grade 6',' Grade 6'),('Grade 7',' Grade 7'),('Grade 8',' Grade 8'),('Grade 8',' Grade 8'),
		('Grade 9',' Grade 9'),('Grade 10',' Grade 10'),('Grade 11',' Grade 11'),('Grade 12',' Grade 12'),
		('Grade 13',' Grade 13')
	)
	level = models.CharField(max_length=10, choices = level_choices)
	
	percentage = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(100)])
	
	group_choice = (
		('A', 'a'),
		('B', 'b'),
		('C', 'c'),
		('D', 'd')
	)
	group = models.CharField(max_length=3, choices=group_choice)
	
class Graph():
	subject_choice = (
		('Math', 'math'),
		('Reading', 'reading')
	)   
	subject = models.CharField(choices=subject_choice, max_length=10)	
	worksheets = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(100)])
	
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	
	kumon_levelM_choices = (
		('9A','9A'),('8A','8A'),('7A','7A'),('6A','6A'),('5A','5A'),
		('4A','4A'),('3A','3A'),('2A','2A'),('A','A'),('B','B'),
		('C','C'),('D','D'),('E','E'),('F','F'),('G','G'),
		('H','H'),('I','I'),('J','J'),('K','K'),('L','L'),
		('M','M'),('N','N'),('O','O'),('X','X'),
	)
	
	kumon_levelR_choices = (
		('7A','7A'),('6A','6A'),('5A','5A'),
		('4A','4A'),('3A','3A'),('2A','2A'),
		('AI','AI'),('AII','AII'),('BI','BI'),('BI','BII'),
		('CI','CI'),('CII','CII'),('DI','DI'),('DI','DII'),
		('EI','EI'),('EII','EII'),('FI','FI'),('FI','FII'),
		('GI','GI'),('GII','GII'),('HI','HI'),('HI','HII'),
		('II','II'),('III','III'),('J','J'),('K','K'),('L','L'),
	)
	
	kumon_levelM = models.CharField(max_length=50, choices = kumon_levelM_choices, default = '9A')
	kumon_levelR = models.CharField(max_length=50, choices = kumon_levelR_choices, default = '7A')
	