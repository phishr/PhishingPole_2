from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('BetaSignup/',views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/UpdateAccount/', views.UpdateAccount, name='UpdateAccount'),
    path('dashboard/UpdateAccount/ChangePassword', views.ChangePassword, name='ChangePassword'),
    #DONT FORGET TO MAKE SURE THAT ALL OF THE LINKS IN THE DASHBOARD WORK
    path('PHISHED/',views.PHISHED,name='PHISHED'),
    path('PHISHED/<employee_id>/',views.PHISHED,name='PHISHED'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    #path('dashboard/trial/', views.trial, name='trial'),
    path('dashboard/individuals/',views.dashboard_individuals,name='dashboard_individuals'),
    path('dashboard/individuals/<target_name>/',views.dashboard_individuals,name='dashboard_individuals'),
    path('dashboard/AddEmployees/', views.AddEmployees,name='AddEmployees'),
    path('dashboard/RemoveEmployees/', views.RemoveEmployees,name='RemoveEmployees'),
    path('dashboard/RemoveEmployees/<employee_name>/', views.RemoveEmployees,name='RemoveEmployees'),
    path('dashboard/campaigns/', views.ViewCampaigns,name='ViewCampaigns'),
    path('dashboard/campaigns/<campaign_name>/', views.ViewCampaigns,name='ViewCampaigns'),
    path('CampaignManager/',views.CampaignManager,name="CampaignManager"),
    #path('CampaignManager/download/<path>/',views.download,name="download"),

    #path('deleteme/',views.DELETEME,name='deleteme')
]