from django.contrib import admin
from .models import Student, StudentBulkUpload

# Register your models here.

admin.site.register(Student)	
admin.site.register(StudentBulkUpload)	