from django import forms
from django.core.validators import RegexValidator
from .models import User, Student, Teacher, Schedule

class DateInput(forms.DateInput):
    input_type = 'date'



class LoginForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['username', 'password']
		widgets = {
			'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
			'username':forms.TextInput(attrs={'placeholder': 'Username'}),

		}

class StudentForm(forms.ModelForm):

	class Meta:
		model = Student
		fields = ['name','nickname','birthdate','age',
                          'gender','picture','phone_num','tel_num',
                          'address','email','student_num','school',
                          'school_level','date_enrolled','kumon_levelM','kumon_levelR','guardian_name',
                          'relation','guardian_num','guardian_email'
                ]
		widgets = {
            'birthdate': DateInput(),
			'date_enrolled': DateInput(),
        }


class TeacherForm(forms.ModelForm):

	class Meta:
		model = Teacher
		fields = ['name','phone_num','tel_num','email','birthdate','age','gender','address','subject','t_picture']
		
		widgets = {
			'birthdate':DateInput(),
		}

class ScheduleForm(forms.ModelForm):
	
	class Meta:
		model = Schedule
		fields = ['teacher','day','timeslots']