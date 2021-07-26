from django.db import models
from users.models import CustomUser

# Create your models here.
class CompanyProfile(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	business_stream_name = models.CharField(max_length=100)
	establishment_date = models.DateField()
	website_url = models.URLField(max_length=200)
	company_profile = models.ImageField(upload_to='company_profile/', null=True, blank=True)
	is_delete = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


	def __str__(self):
		return self.name




class Job(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	companyprofile_id = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
	title = models.CharField(max_length=300)
	description = models.TextField()
	salary = models.IntegerField(null=True)
	experience = models.IntegerField(null=True)
	location = models.CharField(max_length=300)
	category = models.CharField(max_length=100, null=True)
	last_date = models.DateField()
	is_delete = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


	def __str__(self):
		return self.title


gender_choice = (
		('male','Male'),
		('female','Female'),
	)

class Candidate(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	dob = models.DateField(null=True)
	gender = models.CharField(max_length=100, choices=gender_choice, null=True, default=None)
	mobile = models.CharField(max_length=200, null=True)
	resume = models.FileField(upload_to='resume/', null=True)
	job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True)





