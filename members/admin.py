from django.contrib import admin

from .models import Application, Job, JobSeeker, company


@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
	list_display = ('seekerid', 'name', 'email', 'phone')
	search_fields = ('name', 'email', 'phone')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
	list_display = ('jobid', 'title', 'company', 'location', 'salary')
	search_fields = ('title', 'company', 'location')


@admin.register(company)
class CompanyAdmin(admin.ModelAdmin):
	list_display = ('companyid', 'companyname', 'email', 'location')
	search_fields = ('companyname', 'email', 'location')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
	list_display = ('applicationid', 'seeker', 'job', 'status')
	list_filter = ('status',)
