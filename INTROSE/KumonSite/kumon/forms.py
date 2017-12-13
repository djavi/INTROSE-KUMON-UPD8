from django import forms
from django.core.validators import RegexValidator
from .models import User, Student, Teacher, Schedule, sTime, tTime

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

	address = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = Student
		fields = ['lastname', 'firstname', 'middlename', 'nickname','birthdate','gender','picture',
						  'phone_num','tel_num','email',
                          'address','student_num','school',
                          'school_level','date_enrolled', 'status', 'kumon_levelM','kumon_levelR',
                          'guardian_name','relation','guardian_num','guardian_email'
                ]
		widgets = {
            'birthdate': DateInput(),
			'date_enrolled': DateInput(),
        }

class EditStudentForm(forms.ModelForm):

	address = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = Student
		fields = ['nickname','picture',
						  'phone_num','tel_num','email',
                          'address','student_num','school',
                          'school_level','date_enrolled', 'status', 'kumon_levelM','kumon_levelR',
                          'guardian_num','guardian_email']


class TeacherForm(forms.ModelForm):

	class Meta:
		model = Teacher
		fields = ['lastname', 'firstname', 'middlename','phone_num','tel_num','email','birthdate','age','gender','address','subject','t_picture']
		
		widgets = {
			'birthdate':DateInput(),
		}
		
class EditTeacherForm(forms.ModelForm):

	class Meta:
		model = Teacher
		fields = ['phone_num','tel_num','email','address','subject','t_picture']


class ScheduleForm(forms.ModelForm):
	
	class Meta:
		model = Schedule
		fields = ['teacher','day','timeslots']


class sTimeForm(forms.ModelForm):

	class Meta:
		model = sTime
		fields = ['student']

		widgets = {
			
		}
