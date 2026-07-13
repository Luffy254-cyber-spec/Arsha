from django.contrib import admin

from myapp.models import *
# Register your models here.
admin.site.site_header = "Genesis Administration"
admin.site.site_title = "Genesis Admin"
admin.site.index_title = "Welcome to Genesis Dashboard"
admin.site.register(Contact)
admin.site.register(Employee)
