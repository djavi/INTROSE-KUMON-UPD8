from django.contrib import admin

# Register your models here.
from .models import User,Student,Teacher,Schedule,sTime,tTime

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Schedule)
admin.site.register(sTime)
admin.site.register(tTime)