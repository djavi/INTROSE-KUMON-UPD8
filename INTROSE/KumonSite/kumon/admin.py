from django.contrib import admin

# Register your models here.
from .models import User,Student,Teacher,Schedule,sTime,tTime,Tuition,savedTuition,Salary,delEntry,addEntry,tAddEntry,tDelEntry

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Schedule)
admin.site.register(sTime)
admin.site.register(tTime)
admin.site.register(Tuition)
admin.site.register(savedTuition)
admin.site.register(Salary)
admin.site.register(delEntry)
admin.site.register(addEntry)
admin.site.register(tDelEntry)
admin.site.register(tAddEntry)