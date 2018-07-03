import sys
import os

with open("phishr/models.py", "a") as models_file:
				models_file.write("""

class %s(models.Model):
	name = models.CharField(max_length=75)
	company_id = models.CharField(max_length=100)
	clicked_link = models.BooleanField(default=False)
	employee_id = models.CharField(max_length=64,default='DEFAULT')
    				""" % (sys.argv[1],))

os.system("python manage.py makemigrations")

os.system("python manage.py migrate")