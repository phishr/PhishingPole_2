from django.db import models
from django.http import HttpResponse, HttpResponseRedirect, Http404
from Phishr.models import target, phishr_user
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from datetime import datetime
from Phishr.models import target
from Phishr.models import phishr_user
from Phishr.models import campaign_results
from Phishr.models import campaign_directory
import hashlib
import os
import pickle
from django.apps import apps
from django.conf import settings
import json
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db import connection as MYSQL_CONNECTION
import pickle

'''
for C in campaign_directory.objects.all():
	exec("global " + C.campaign_name)
	exec(C.campaign_name+' = apps.get_model("Phishr","'+ C.campaign_name +'")') 
'''

### FUNCTIONS THAT ARE NOT VIEWS ###

#def target_isnt_too_young(target):
	#check if a target has existed for long enough to have been sent a phishing email

def get_email(name,CID):
	try:
		return target.objects.filter(name=name,company_id=CID)[0].email
	except:
		return 'NONE'

def create_employee_id(name,CID,campaign_name):
	return hashlib.sha224(str(name+CID+campaign_name).encode('utf-8')).hexdigest()
'''
def user_has_trial_targets(user):
	exec(str(get_company_id(user.username)+'_trial_campaign')+' = apps.get_model("Phishr","'+ str(get_company_id(user.username)+'_trial_campaign') +'")')
	exec('user_trial_campaign = '+ str(get_company_id(user.username)+'_trial_campaign') +'.objects.all()')
	if len(locals()['user_trial_campaign']) > 0:
		return True
	else:
		return False
'''

def is_trial_user(user):
	return phishr_user.objects.filter(username=user.username,company_id=get_company_id(user.username))[0].trial_user

def campaigns_witnessed(user):
	a = []
	b = []
	return_value = []
	for campaign in campaign_results.objects.filter(company_id=get_company_id(user.username)):
		a.append(campaign)

	for campaign in a:
		if campaign.campaign_name in b:
			pass
		else:
			return_value.append(campaign)
			b.append(campaign.campaign_name)
	
	return return_value


def campaigns_attempted_on_target(target):
	return_value = []
	for campaign in campaign_results.objects.filter(company_id=target.company_id,name=target.name):
		return_value.append(campaign)
	return return_value


		
def get_join_date(user):
	most_distant_date = datetime.today()
	most_distant_date = datetime.date(most_distant_date)
	for T in target.objects.filter(company_id=get_company_id(user.username)):
		if T.join_date < most_distant_date:
			most_distant_date = T.join_date
		else:
			pass

	return most_distant_date



def target_email_in_use(email,CID):
	if len(target.objects.filter(email=email,company_id=CID)) > 0:
		return True
	else:
		return False


def target_exists(name,CID):
	if len(target.objects.filter(name=name,company_id=CID)) > 0:
		return True
	else:
		return False

def replace_chars(string):
	L = list(string)
	for char in L:
		if char == "/" or "\\" or "<" or " ":
			if char == " ":
				char = '_'
			else:
				del char
	return ''.join(L) 


#def verify_email(string):


def data_exists_for_user(user):
	most_recent_campaign = campaign_directory.objects.filter().latest('campaign_date')
	a = campaign_results.objects.filter(campaign_name=most_recent_campaign.campaign_name,company_id=get_company_id(user.username))
	if len(a) > 0:
		return True
	else:
		return False

def user_has_targets(user):
	for t in target.objects.all():
		if t.company_id == get_company_id(user.username):
			return True
		else:
			pass
	return False


def username_present(username):
    if User.objects.filter(username=username).exists():
        return True
    
    return False

def email_present(email):
    if User.objects.filter(email=email).exists():
        return True
    
    return False

def cname_present(cname):
    if phishr_user.objects.filter(company_id=cname).exists():
        return True
    
    return False

def get_company_id(username):
	if username == '':
		return 'N/A'
	else:
		return phishr_user.objects.filter(username=username)[0].company_id

def get_company_name(username):
	if username == '':
		return 'N/A'
	else:
		random_target = target.objects.filter(company_id=get_company_id(username))[0]
		return random_target.company_name

def reformat_name(name):
	test = 0
	new = []
	for l in list(name):
		if l.isupper():
			test = test + 1
			if test >= 2:
				new.append(' ')
				new.append(l)
			else:
				new.append(l)
		else:
			new.append(l)
	return ''.join(new)

def name_to_target_object(n,r):
	return_value = target.objects.filter(name=n,company_id=r)[0]
	return return_value

def get_number_bamboozled(campaign_name,CID,request):
	return_value = 0
	for t in campaign_results.objects.filter(campaign_name=campaign_name,company_id=CID):
		if t.clicked_link == True:
			return_value = return_value + 1
		else:
			pass

	return return_value

def check_if_bamboozled(T,CAMPAIGN,request):
	for c in campaign_results.objects.filter(name=T.name,campaign_name=CAMPAIGN.campaign_name,company_id=get_company_id(request.user.username)):
		if c.clicked_link:
			return True
		else:
			return False


def CNAME_TO_CID(string):
	return_value = []
	for letter in string:
		if letter == ' ':
			pass
		else:
			return_value.append(letter)
	return ''.join(return_value)


def CID_TO_CNAME(string):
	return ''.join(string.split(" "))


def format_graph_data(request,sign_up_date,individual=False,T=None):
	#return_value = ['[0, 0]','[1, 10]','[2, 20]','[3, 22]','[4, 30]']
	return_value = []
	i = 0
	if individual == False:

		if get_join_date(request.user) < campaign_directory.objects.filter().latest('campaign_date').campaign_date:

			
			for campaign in campaigns_witnessed(request.user):
				
				appendme = str("["+str(i)+', '+str(get_number_bamboozled(campaign_name=campaign.campaign_name,request=request,CID=get_company_id(request.user)))+']')
				
				return_value.append(appendme)

				i = i + 1

			return ','.join(return_value)

		else:
			return_value = '[0, 1], [1, 1]'
			return return_value



	else:

		if T.join_date < campaign_directory.objects.filter().latest('campaign_date').campaign_date:
			
			most_recent_campaign = campaign_directory.objects.filter().latest('campaign_date')
			
			for campaign in campaigns_attempted_on_target(T):
				
				if check_if_bamboozled(T=T,CAMPAIGN=campaign,request=request):
					appendme = str("["+str(i)+', 1]')
					return_value.append(appendme)

					i = i + 1
				
				else:
					appendme = str("["+str(i)+', 0]')
					return_value.append(appendme)

					i = i + 1



			return ','.join(return_value)

		else:
			return_value = '[0, 1], [1, 1]'
			return return_value


def get_time_signed_up(request):
	#this function is to be used to return NUMBER OF CAMPAIGNS SIGNED UP FOR, NOT NUMBER OF MONTHS SIGNED UP.
	used = []
	return_value = 0

	for campaign in campaign_results.objects.filter(company_id=get_company_id(request.user.username)):
		if campaign.campaign_name not in used:
			used.append(campaign.campaign_name)
			return_value = return_value + 1
		else:
			pass

	return return_value

### END FUNCTIONS THAT ARE NOT VIEWS ###



@login_required(login_url='/login/')
def logout(request):
	'''if request.user.is_authenticated:'''
	django_logout(request)
	return HttpResponseRedirect('/login/')
	'''else:
		return HttpResponse("You're already logged out.")'''

def home(request):

	return render(request, 'phishr/home.html',{
		'request': request,
		})

@login_required(login_url='/login/')
def dashboard(request):

	if request.user.username == 'admin':
			return HttpResponseRedirect('/admin_dashboard/')

	elif is_trial_user(request.user):
		return HttpResponseRedirect("/dashboard/trial/")

	else:

		if request.user.username == '':
			return HttpResponseRedirect('/login/')
					#later I'll figure out something I can do with the extra 
		else:

			#get who clicked on most recent campaign

			#make sure user has more than one target

			if user_has_targets(request.user):

				if data_exists_for_user(request.user):

					most_recent_campaign = campaign_directory.objects.filter().latest('campaign_date')
					recent_list = campaign_results.objects.filter(campaign_name=most_recent_campaign.campaign_name,company_id=get_company_id(request.user.username))
					recent_vulnerable_targets = 0
					recent_nonvulnerable_targets = 0
					for T in recent_list:
						if T.clicked_link == True:
							recent_vulnerable_targets = recent_vulnerable_targets + 1
						else:
							recent_nonvulnerable_targets = recent_nonvulnerable_targets + 1


					#get the total average
					average_vulnerable_targets = 0
					average_nonvulnerable_targets = 0
					campaigns = campaign_directory.objects.all()
					for c in campaigns:
						all_campaigns = campaign_results.objects.filter(company_id=get_company_id(request.user.username))
						for T in all_campaigns:
							if T.clicked_link:
								average_vulnerable_targets = average_vulnerable_targets + 1
							else:
								average_nonvulnerable_targets = average_nonvulnerable_targets + 1
					
					#average
					average_vulnerable_targets = average_vulnerable_targets/get_time_signed_up(request)
					average_nonvulnerable_targets = average_nonvulnerable_targets/get_time_signed_up(request)


					#generate graph data in this format: [0, 0],[1, 10],[2,20],[3,22]

					error_message = ''

					if len(campaigns_witnessed(request.user)) < 2:
						error_message = '*Your account has existed for too little time to see any meaningful data.'

					elif len(target.objects.filter(company_id=get_company_id(request.user.username))) < 2:
						error_message = '*You have too few employees signed up to see any meaningful data.'


					return render(request, 'phishr/dashboard/dashboard_home.html',{
							'error_message': error_message,
							'formated_graph_data': format_graph_data(request,get_time_signed_up(request)),
							'recent_vulnerable_targets': recent_vulnerable_targets,
							'recent_nonvulnerable_targets': recent_nonvulnerable_targets,
							'average_vulnerable_targets': average_vulnerable_targets,
							'average_nonvulnerable_targets': average_nonvulnerable_targets,
							'user': request.user,
							'request': request,
							})
				else:
					return render(request,'phishr/dashboard/NO_DATA.html')
					
			else:
				return render(request, 'phishr/dashboard/NO_TARGETS.html')
	
@login_required(login_url='/login/')
def dashboard_individuals(request, target_name=''):

	if request.user.username == 'admin':
			return HttpResponseRedirect('/admin_dashboard/')

	elif is_trial_user(request.user):
		return HttpResponseRedirect("/dashboard/trial/")

	else:

		if request.user.username == '':
			return HttpResponseRedirect('/login/')
				#later I'll figure out something I can do with the extra 
		else:

			if user_has_targets(request.user):

				if target_name == '':

					target_list = target.objects.filter(company_id=phishr_user.objects.filter(username=request.user.username)[0].company_id)

					return render(request, 'phishr/dashboard/individuals.html',{
							'individual' : False,
							'user': request.user,
							'request': request,
							'employees': target_list,
							})

				else:
					#check if name is in database FOR USER
					if data_exists_for_user(request.user):

						individual_target = get_object_or_404(target, name=reformat_name(target_name))

						campaigns = []
				
						clicks = {}
						
						print('length = :' + str(len(campaign_directory.objects.filter(campaign_date__range=[datetime.date(datetime.today()),get_join_date(request.user)]))))

						for C in campaign_directory.objects.all():
							if C.campaign_date < get_join_date(request.user):
								pass
							else:
								try:
									print('company_id = '+get_company_id(request.user.username)+"\n name = "+reformat_name(target_name)+"\n campaign_name = "+C.campaign_name)
									c = campaign_results.objects.filter(company_id=get_company_id(request.user.username),name=reformat_name(target_name),campaign_name=C.campaign_name)
									clicks[C.campaign_name] = c[0].clicked_link
									campaigns.append(C)



								except:
									pass
								
						if len(clicks) == 0:
							return render(request,'phishr/dashboard/NO_DATA_USER.html')
						else:
							pass

								
						print('\n\nreturning clicks = '+ str(clicks) +' \ncampaigns = '+str(campaigns)+"\n\n")
						return render(request, 'phishr/dashboard/individuals.html',{
								'clicks': clicks,
								'campaigns': campaigns,
								'individual' : True,
								'TARGET': individual_target,
								'user': request.user,
								'request': request,
								'formated_graph_data': format_graph_data(request,get_time_signed_up(request),individual=True,T=individual_target)
								})
					else:
						return render(request,'phishr/dashboard/NO_DATA.html')

			else:
				return render(request, 'phishr/dashboard/NO_TARGETS.html')

def register(request):
	#make sure names get capitalized eventually lol
	if request.user.is_authenticated:
		#tell user they are logged in with link to dashboard
		return HttpResponse('You are already logged in. Click <a href="/logout/">here</a> to log out.')

	else:
		if 'username' and 'password' and 'password_confirmation' and 'company_name' and 'email' and 'first_name' and 'last_name' in request.POST:
			#add password confirmation to make sure that they're the same
			username = request.POST['username']
			password = request.POST['password']
			password_confirmation = request.POST['password_confirmation']
			company_name = request.POST['company_name']
			email = request.POST['email']
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']

			company_id = []
			for letter in list(company_name):
				if letter != ' ':
					company_id.append(letter)
				else:
					pass

			if username_present(username):
				return render(request, 'phishr/register.html',{
				'error_message': "Username already exists.",
				})

			else:

				if email_present(email):
					return render(request, 'phishr/register.html',{
					'error_message': "Email already in use.",
					})
				else:
					if cname_present(''.join(company_id)):
						#make entry with same company name but with a 2 at the end and so on
						company_id.append(username)
					else:
						pass
					if password == password_confirmation:
						#make account normally
						new_Puser = phishr_user()

						new_Puser.username = username
						new_Puser.company_id = ''.join(company_id)
						new_Puser.save()


						user = User.objects.create_user(username=username,
	                                 email=email,
	                                 password=password,
	                                 first_name=first_name,
	                                 last_name=last_name,)

						return HttpResponseRedirect('/login/')
					else:
						return render(request, 'phishr/register.html',{
							'error_message': 'passwords do not match',
							})
		
		else:
			return render(request, 'phishr/register.html')


# Always return an HttpResponseRedirect after successfully dealing

'''
for test logins:
	username: John_doe
	password: johnspassword
'''

#make ability to log in with email too
def login(request): 

	if request.user.is_authenticated:
		#tell user they are logged in with link to dashboard
		return HttpResponseRedirect("/dashboard/")

	else:
		if 'username' and 'password' in request.POST: #['username'] and request.POST['password'] in request.POST:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(request, username=username, password=password)

			if user is not None:
				django_login(request, user)
				return HttpResponseRedirect('/dashboard/')
			
			else:

				return render(request, 'phishr/login.html',{
					'error_message': "Incorrect Login.",
					})

		else:
			return render(request, 'phishr/login.html')

@login_required(login_url='/login/')
def UpdateAccount(request):

	if request.user.username == 'admin':
			return HttpResponseRedirect('/admin_dashboard/')

	elif is_trial_user(request.user):
		return HttpResponseRedirect("/dashboard/trial/")

	else:
		
		if request.user.username == '':
			return HttpResponseRedirect('/login/')

		else:

			if user_has_targets(request.user):

				if 'new_username' and 'new_company_name' and 'new_email' and 'new_first_name' and 'new_last_name' in request.POST:

					new_username = request.POST['new_username']
					new_company_name = request.POST['new_company_name']
					new_email = request.POST['new_email']
					new_first_name = request.POST['new_first_name']
					new_last_name = request.POST['new_last_name']

					old_username = request.user.username
					old_company_id = get_company_id(request.user.username)
					old_company_name = get_company_name(request.user.username)

					#update phishing campaigns
					for i in range(len(campaign_directory.objects.all())):
						CAMPAIGN = campaign_results.objects.filter(company_id=old_company_id)
						for c in CAMPAIGN:
							if c.company_id == old_company_id:
								c.company_id = CNAME_TO_CID(new_company_name)
								c.save()
							else:
								pass
						
					#update targets works!
					for t in target.objects.all():
						T = target.objects.get(name=t.name,company_id=t.company_id)
						T.company_name = new_company_name
						T.company_id = CNAME_TO_CID(new_company_name)
						T.save()

					#update users and phishr_users
					User.objects.filter(username=request.user.username).update(username=new_username,email=new_email,first_name=new_first_name,last_name=new_last_name)
					phishr_user.objects.filter(username=request.user.username,company_id=get_company_id(request.user.username)).update(username=new_username,company_id=CNAME_TO_CID(new_company_name))

					return render(request, 'phishr/Edit_account_info_pretty.html', {
						'error_message': 'account info updated successfully',
						'user': request.user,
						'request': request,
						})

				else:
					return render(request, 'phishr/Edit_account_info_pretty.html',{
						'user': request.user,
						'company_name': get_company_name(request.user.username),
						'request': request,
						})
			else:
				return render(request, 'phishr/dashboard/NO_TARGETS.html')

@login_required(login_url='/login/')
def ViewCampaigns(request, campaign_name=''):

	if request.user.username == 'admin':
			return HttpResponseRedirect('/admin_dashboard/')

	elif is_trial_user(request.user):
		return HttpResponseRedirect("/dashboard/trial/")

	else:

		if request.user.username == '':
			return HttpResponseRedirect('/login/')
		
			#later I'll figure out something I can do with the extra 
		else:

			if user_has_targets(request.user):

				if campaign_name == '':

					campaigns = []
					
					for C in campaign_directory.objects.all():
						if C.campaign_date < get_join_date(request.user):
							pass
						else:
							campaigns.append(C)

					return render(request, 'phishr/dashboard/campaigns.html',{
							'individual' : False,
							'user': request.user,
							'request': request,
							'campaigns': campaigns,
							})

				else:

					if data_exists_for_user(request.user):

						#let the user see the strategy of the campaign and the information given

						try:
							individual_campaign = campaign_results.objects.filter(company_id=get_company_id(request.user.username),campaign_name=campaign_name)

						except:
							pass

						if len(individual_campaign) <= 0:
							raise Http404("campaign does not exist")

						else:
							#display a pie chart and a list of employees

							vulns_number = 0
							nonvulns_number = 0

							for T in individual_campaign:
								
								if T.clicked_link == True:
									vulns_number = vulns_number + 1

								else:
									nonvulns_number = nonvulns_number + 1





							return render(request, 'phishr/dashboard/campaigns.html',{
								'campaign_name': campaign_name,
								'campaign_nonvulnerable_targets': nonvulns_number,
								'campaign_vulnerable_targets': vulns_number,
								'individual' : True,
								'user': request.user,
								'request': request,
								'campaign_targets': locals()["individual_campaign"].filter(company_id=get_company_id(request.user.username)),
								})
					else:
						return render(request,'phishr/dashboard/NO_DATA.html')

			else:
				return render(request, 'phishr/dashboard/NO_TARGETS.html')


@login_required(login_url='/login/')
def AddEmployees(request):
	
	if request.user.username == 'admin':
		return HttpResponseRedirect('/admin_dashboard/')

	elif request.user.username == '':
		return HttpResponseRedirect('/login/')

	else:
		if 'email' and 'first_name' and 'last_name' and 'phone_number' in request.POST:
				
			if target_exists(name=str(request.POST['first_name'] + " " + request.POST['last_name']),CID=get_company_id(request.user.username)):

				return render(request, 'phishr/add_target.html',{
					'error_message': 'Employee name already in use. No changes made.'
					})

			elif target_email_in_use(email=request.POST['email'],CID=get_company_id(request.user.username)):

				return render(request, 'phishr/add_target.html', {
					'error_message': "Email already in use. No changes made."
					})

			else:

								#add password confirmation to make sure that they're the same
				company_ID = get_company_id(request.user.username)
				email = request.POST['email']
				first_name = request.POST['first_name']
				last_name = request.POST['last_name']
				phone_number = request.POST['phone_number']
				join_date = datetime.today().strftime('%Y-%m-%d')


				namelist = [first_name,last_name]

				new_target = target(company_id=company_ID,name=' '.join(namelist),company_name=CID_TO_CNAME(company_ID),join_date=join_date,email=email,phone_number=phone_number)
				
				new_target.save()

				return render(request,'phishr/add_target.html',{
						'error_message': "Target added successfully!"
						})


		else:
			return render(request, 'phishr/add_target.html')

@login_required(login_url='/login/')
def RemoveEmployees(request,employee_name=''):
	if request.user.username == 'admin':
			return HttpResponseRedirect('/admin_dashboard/')

	elif is_trial_user(request.user):
		return HttpResponseRedirect("/dashboard/trial/")

	else:

		if request.user.username == '':
			return HttpResponseRedirect('/login/')
				#later I'll figure out something I can do with the extra 
		else:

			if user_has_targets(request.user):

				if 'employee_name' and "delete" in request.POST and request.POST["delete"] == "yes":
					
					t = target.objects.get(name=request.POST['employee_name'],company_id=get_company_id(request.user.username))
					t.delete()

					return HttpResponseRedirect("/dashboard/RemoveEmployees/", {
						"error_message": "Employee successfully deleted."
						})

				else:

					if employee_name == '':

						target_list = target.objects.filter(company_id=phishr_user.objects.filter(username=request.user.username)[0].company_id)

						return render(request, 'phishr/dashboard/remove_employee.html',{
								'individual' : False,
								'user': request.user,
								'request': request,
								'employees': target_list,
								})

					else:
						#check if name is in database FOR USER
						individual_target = get_object_or_404(target, name=reformat_name(employee_name))

						return render(request, 'phishr/dashboard/remove_employee.html',{
								'individual' : True,
								'TARGET': individual_target,
								'user': request.user,
								'request': request,
								})
			else:
				return render(request, 'phishr/dashboard/NO_TARGETS.html')


def admin_dashboard(request):
	if request.user.username == 'admin':

		return render(request, 'phishr/dashboard/admin_dashboard.html')

	else:
		return HttpResponseRedirect("/dashboard/")

def create_user(request):
	if request.user.username == 'admin':


		return render(request, 'phishr/dashboard/create_user.html')

	else:
		return HttpResponseRedirect("/dashboard/")


def create_trial_user(request):
	return HttpResponse("Create Trial Users Here")


@login_required
def download(request, path=None):
	if request.user.username == 'admin':
	    
	    file_path = os.path.join(settings.MEDIA_ROOT, path)
	    if os.path.exists(file_path):
	        with open(file_path, 'rb') as fh:
	            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
	            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
	            return response
	    raise Http404
	
	else:
		return HttpResponseRedirect('dashboard')


class new_model():
	name = models.CharField(max_length=75)
	company_id = models.CharField(max_length=100)
	clicked_link = models.BooleanField(default=False)
	employee_id = models.CharField(max_length=64,default='DEFAULT')


@login_required(login_url='/login/')
def CampaignManager(request):
	if request.user.username == 'admin':
		
		if 'name' and 'description' in request.POST:
			campaign_name = request.POST['name']
			campaign_description = request.POST['description']

			print('cerating new campaign: ' + campaign_name)

			new_campaign = campaign_directory(campaign_date=datetime.date(datetime.today()),campaign_name=campaign_name,description=campaign_description)
			new_campaign.save()

			#fill campaign results here
			for t in target.objects.all():
				a = campaign_results(campaign_name=campaign_name,name=t.name,company_id=t.company_id,employee_id=create_employee_id(t.name,t.company_id,campaign_name))
				a.save()

			return render(request,"phishr/CampaignManager.html",{
				'error_message': 'campaign successfully added',
				})


		else:

			return render(request, 'phishr/CampaignManager.html')




	else:
		return HttpResponseRedirect("/dashboard/")
'''
@login_required(login_url='/login/')
def trial(request):

	if is_trial_user(request.user):

		if user_has_trial_targets(request.user):
	
			try:
				print('database name: '+str(get_company_id(request.user.username)+'_trial_campaign'))
				exec(str(get_company_id(request.user.username)+'_trial_campaign')+' = apps.get_model("Phishr","'+ str(get_company_id(request.user.username)+'_trial_campaign') +'")')
				exec('user_trial_campaign = '+ str(get_company_id(request.user.username)+'_trial_campaign') +'.objects.all()')

			except:
				return render(request, 'phishr/dashboard/Trial_dashboard.html',{
					'error_message': 'Unable to find data for your trial campaign, please contact us for support: support@phishr.io'
					})

			vulns_number = 0
			nonvulns_number = 0



			for T in locals()['user_trial_campaign'].filter(company_id=get_company_id(request.user.username)):
									
				if T.clicked_link == True:
					vulns_number = vulns_number + 1

				else:
					nonvulns_number = nonvulns_number + 1


			return render(request, 'phishr/dashboard/campaigns.html',{
				'campaign_nonvulnerable_targets': nonvulns_number,
				'campaign_vulnerable_targets': vulns_number,
				'user': request.user,
				'request': request,
				'campaign_targets': locals()["user_trial_campaign"].filter(company_id=get_company_id(request.user.username)),
							})

		else:
			return render(request, 'phishr/dashboard/NO_TARGETS.html')

	else:
		return HttpResponseRedirect("/dashboard/")
'''

@login_required(login_url='/login/')
def ChangePassword(request,userid=''):
	if request.user.username == 'admin':
		return HttpResponseRedirect('/admin_dashboard/')

	elif is_trial_user(request.user):
		return HttpResponseRedirect("/dashboard/trial/")

	else:
		
		if request.user.username == '':
			return HttpResponseRedirect('/login/')

		else:

			if user_has_targets(request.user):

				if 'new_password' and 'new_password_confirmation' in request.POST:

					if request.POST['new_password'] == request.POST['new_password_confirmation']:
						u = User.objects.get(username__exact=request.user.username)
						u.set_password(request.POST['new_password'])
						u.save()

						return render(request, 'phishr/ChangePassword.html', {
							'error_message': 'password changed successfully',
							'user': request.user,
							'request': request,
							})
					else:
						return render(request, 'phishr/ChangePassword.html', {
							'error_message': 'passwords do not match.',
							'user': request.user,
							'request': request,
							})

				else:
					return render(request, 'phishr/ChangePassword.html',{
						'user': request.user,
						'company_name': get_company_name(request.user.username),
						'request': request,
						})
			else:
				return render(request, 'phishr/dashboard/NO_TARGETS.html')


def PHISHED(request,employee_id=''):
	#The Id will be the hash of the campaign name + the targets name together
	#this is the code for when a target clicks on a phishinhg link\
	if employee_id != '':
		for target in campaign_results.objects.all():
			if target.employee_id == employee_id:
				target.clicked_link = True
				target.save()

				return render(request, 'phishr/PHISHED.html',{
					'target': name_to_target_object(target.name,target.company_id)
					})

			else:
				pass
		return Http404()
	else:
		HttpResponseRedirect("/")

#some code for making test database entries and editing things when I fuck up


def DELETEME(request):
	for campaign in campaign_directory.objects.all():
		exec('c = '+campaign.campaign_name+'.objects.all()')
		for t in locals()['c']:
			a = campaign_results()
			a.name = t.name
			a.campaign_name = campaign.campaign_name
			a.company_id = t.company_id
			a.clicked_link = t.clicked_link
			a.employee_id = create_employee_id(t.name,t.company_id,campaign.campaign_name)
			a.save()


	return HttpResponse("done")



def beta_signup(request):
	return HttpResponse('beta_signup')



'''
def contact(request): #here I'll put contact info

def update_account(request): #change name, company, add or remove employees ... etc
'''