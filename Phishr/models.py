from django.db import models
from django.contrib.auth.models import User


#create recovery code upon creation of new user
#create new recovery code after password change
#use email provided to find user
class passwordrecovery(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	reset_code = models.CharField(max_length=6)

class company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(default="NOT-SET",max_length=100)

class target(models.Model):
	'''
    example_target = target(name="John Doe",email="johndoe@example.com",phone_number="N/A",company_id="ExampleInc",company_name="Example Inc",TEMP_CAMPAIGN_RECORDS="2001-05-16")
	'''
	name = models.CharField(max_length=75)
	email = models.EmailField()
	phone_number = models.CharField(max_length=13)
	company_id = models.CharField(max_length=100)
	company_name = models.CharField(max_length=100)
	join_date = models.DateField()

class phishr_user(models.Model):
	paid = models.BooleanField(default=False)
	username = models.CharField(max_length=200)
	company_id = models.CharField(max_length=100)


class campaign_directory(models.Model):
	campaign_name = models.CharField(max_length=75)
	campaign_date = models.DateField()
	description = models.CharField(default="N/A",max_length=200)

class campaign_results(models.Model):
	campaign_name = models.CharField(max_length=75)
	company_id = models.CharField(max_length=100)
	name = models.CharField(max_length=75)
	clicked_link = models.BooleanField(default=False)
	employee_id = models.CharField(max_length=64,default='DEFAULT')


class trial_campaigm_directory:
	campaign_name = models.CharField(max_length=75)
	campaign_date = models.DateField()
	company_id = models.CharField(max_length=100)



	#I need to figure out a way to show if they have clicked on the link or not for the past 3 years
	#for a demonstration, I'll start with a characterstring of 200 zeros and ones representing each
	#campaign and a zero means they didnt click and a one means that they did


#for examples sake I'll start them off with a year for examples and graphig

### PHISHING CAMPAIGNS ###

#new campaigns have to end in the number they are