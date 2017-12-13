from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^create_user/$', views.create_user, name='create'),
    url(r'^home/$', views.home, name='home'), 
	url(r'^students/$', views.studentPage, name='students'),
	url(r'^studprofile/([0-9]+)/$', views.studentProfile, name='student-profile'),
	url(r'^addstudent/$', views.addStudent, name='add-student'),
	url(r'^editstudent/([0-9]+)/$', views.editStudent, name='edit-student'),
	url(r'^editteacher/([0-9]+)/$', views.editTeacher, name='edit-teacher'),
	url(r'^addstudent/$', views.addStudent, name='add-student'),
    url(r'^teachers/$', views.teacherPage, name='teacher'),
    url(r'^teacherprofile/([0-9]+)/$', views.teacherProfile, name='profile'),
    url(r'^attendance/$', views.attendancePage, name='attendance'),
    url(r'^attendance/(?P<date>\d{4}-\d{2}-\d{2})/$', views.attendancePage, name='attUpdate'),
    url(r'^schedule/$', views.schedulePage, name='schedule'),
    url(r'^salaries/$', views.salaryPage, name='salary'),
    url(r'^payments/$', views.paymentPage, name='payments'),
    url(r'^payments/(?P<date>\d{4}-\d{2}-\d{2})/$', views.paymentPage, name='paymentUp'),  
    url(r'^expenses/$', views.expensesPage, name='expenses'),
    url(r'^expenses/(?P<date>\d{4}-\d{2}-\d{2})/$', views.expensesPage, name='expensesUp'),
    url(r'^inventory/$', views.inventoryPage, name='inventory'),
    url(r'^salaries_format/$', views.salaryFormatPage, name='salary_format'),
    url(r'^salaries_format/update/$', views.salaryFormatUpdate, name='salaryUpdate'),  
    url(r'^teacher_salary/([0-9]+)/$', views.teacherSalaryPage, name='teacher_salary'),
    url(r'^teacher_salary/([0-9]+)/pdf$', views.get, name='rendertopdf'),
    url(r'^addteacher/$', views.addTeacher, name='add-teacher'),
    url(r'^inventory/update/$', views.inventoryUpdate, name='inventoryUpdate'),    
    url(r'^inventory/add/$', views.inventoryAdd, name='inventoryAdd'), 
    url(r'^expenses/update/$', views.expensesUpdate, name='expensesUpdate'),
    url(r'^expenses/update/(?P<date>\d{4}-\d{2}-\d{2})/$', views.expensesUpdate, name='exp'),
    url(r'^expenses/add/$', views.exspensesAdd, name='exspensesAdd'),
    url(r'^expenses/add/(?P<date>\d{4}-\d{2}-\d{2})/$', views.exspensesAdd, name='exsp'),

]
