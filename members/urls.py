from django.urls import path
from . import views


urlpatterns = [
   path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('jobseekerregister/', views.jobseekerregister, name='jobseekerregister'),
    path('jobseekerregisterprocess/', views.jobseekerregisterprocess, name='jobseekerregisterprocess'),
   path('jobseekerloginprocess/', views.jobseekerloginprocess, name='jobseekerloginprocess'),
    path('jobseekerlogout/', views.jobseekerlogout, name='jobseekerlogout'),
   path('jobseekerloginprocess/addprofile/', views.addprofile, name='addprofile'),
    path('jobseekerloginprocess/uploadresume/', views.uploadresume, name='uploadresume'),
   path('addprofileprocess/', views.addprofileprocess, name='addprofileprocess'),
    path('jobseekerloginprocess/showprofile/', views.showprofile, name='showprofile'),
    path('deleteprofile/<int:seekerid>/', views.deleteprofile, name='deleteprofile'),
    path('jobseekerloginprocess/searchprofile/', views.searchprofile, name='searchprofile'),
    path('searchprofileprocess/', views.searchprofileprocess, name='searchprofileprocess'),
    path('jobseekerloginprocess/modifyprofile/', views.modifyprofile, name='modifyprofile'),
    path('modifyprofileprocess/', views.modifyprofileprocess, name='modifyprofileprocess'),
    path('jobseekerloginprocess/viewjobs/', views.viewjobs, name='viewjobs'),
    path('jobseekerloginprocess/applyjob/', views.applyjob, name='applyjob'),
    path('applyjobprocess/', views.applyjobprocess, name='applyjobprocess'),
    path('jobseekerloginprocess/viewapplicationstatus/', views.viewapplicationstatus, name='viewapplicationstatus'),
    

    #company

    path('companylogin/',views.companylogin, name='companylogin'),
    path('companyregister/', views.companyregister, name='companyregister'),
    path('companyregisterprocess/', views.companyregisterprocess, name='companyregisterprocess'),
    path('companydashboard/', views.companydashboard, name='companydashboard'),
    path('companylogout/', views.companylogout, name='companylogout'),
    path('companyloginprocess/', views.companyloginprocess, name='companyloginprocess'),
    path('companyloginprocess/addjob/', views.addjob, name='addjob'),
    path('addjobprocess/', views.addjobprocess, name='addjobprocess'),
    path('companyloginprocess/showjobs/', views.showjobs, name='showjobs'),
    path('companyloginprocess/deletejob/', views.deletejob, name='deletejob'),
    path('deletejobprocess/', views.deletejobprocess, name='deletejobprocess'),
    path('companyloginprocess/viewapplications/', views.viewapplications, name='viewapplications'),
    path('acceptapplicationinline/', views.acceptapplicationinline, name='acceptapplicationinline'),
    path('rejectapplicationinline/', views.rejectapplicationinline, name='rejectapplicationinline'),
    path('companyloginprocess/searchjobs/', views.searchjobs, name='searchjobs'),
    path('searchjobsprocess/', views.searchjobsprocess, name='searchjobsprocess'),
    path('companyloginprocess/modifyjob/', views.modifyjob, name='modifyjob'),
    path('modifyjobprocess/', views.modifyjobprocess, name='modifyjobprocess'),

]