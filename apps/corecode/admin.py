from django.contrib import admin
from .models import SiteConfig, AcademicSession,AcademicTerm,Subject,StudentClass,Staff

# Register your models here.

admin.site.register(SiteConfig)	
admin.site.register(AcademicSession)	
admin.site.register(AcademicTerm)	
admin.site.register(Subject)
admin.site.register(StudentClass)
admin.site.register(Staff)	