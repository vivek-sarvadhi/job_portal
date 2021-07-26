from django.contrib import admin
from portal.models import CompanyProfile, Job, Candidate

# Register your models here.

admin.site.register(CompanyProfile)
admin.site.register(Job)
admin.site.register(Candidate)