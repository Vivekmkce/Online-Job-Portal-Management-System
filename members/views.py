from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import JobSeeker,Job,Application,company


MAX_RESUME_SIZE = 2 * 1024 * 1024
ALLOWED_RESUME_EXTENSIONS = ('.pdf', '.doc', '.docx')


def access_denied(request):
    return HttpResponse("Access Denied")


def get_logged_in_jobseeker(request):
    seeker_id = request.session.get('jobseeker_id')
    if not seeker_id:
        return None
    return JobSeeker.objects.filter(seekerid=seeker_id).first()


def get_logged_in_company(request):
    company_id = request.session.get('company_id')
    if not company_id:
        return None
    return company.objects.filter(companyid=company_id).first()


def is_allowed_resume_file(uploaded_file):
    if uploaded_file is None:
        return False

    return uploaded_file.name.lower().endswith(ALLOWED_RESUME_EXTENSIONS)



def home(request):
    return render(request, 'jobseekerlogin.html')


def jobseekerregister(request):
    return render(request, 'jobseekerregister.html')


def companyregister(request):
    return render(request, 'Company/companyregister.html')


def dashboard(request):
    return render(request, 'jobseekerhome.html')


def jobseekerlogout(request):
    request.session.flush()
    return redirect('home')

@csrf_exempt
def jobseekerloginprocess(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = JobSeeker.objects.filter(
            email=email,
            password=password
        ).first()

        if user:
            request.session["jobseeker_id"] = user.seekerid
            return redirect("dashboard")

        return render(request, "jobseekerlogin.html", {"msg": "Login Failed"})

    return render(request, "jobseekerlogin.html")

@csrf_exempt
def jobseekerregisterprocess(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        skills = request.POST.get('skills')
        resume = request.FILES.get('resume')

        if JobSeeker.objects.filter(email=email).exists():
            return render(request, 'jobseekerregister.html', {'msg': 'Email already registered'})

        if resume:
            if not is_allowed_resume_file(resume):
                return render(request, 'jobseekerregister.html', {'msg': 'Only PDF, DOC, or DOCX resumes are allowed.'})

            if resume.size > MAX_RESUME_SIZE:
                return render(request, 'jobseekerregister.html', {'msg': 'Resume size must be 2 MB or less.'})

        JobSeeker.objects.create(
            name=name,
            email=email,
            password=password,
            phone=phone,
            skills=skills,
            resume=resume,
        )
        return redirect('home')

    return render(request, 'jobseekerregister.html')

def addprofile(request):
    user = get_logged_in_jobseeker(request)
    if not user:
        return access_denied(request)

    return render(request, 'uploadresume.html')


def uploadresume(request):
    user = get_logged_in_jobseeker(request)
    if not user:
        return access_denied(request)

    return render(request, 'uploadresume.html')

def addprofileprocess(request):
    if request.method == 'POST':
        user = get_logged_in_jobseeker(request)
        if not user:
            return access_denied(request)

        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Phone = request.POST.get('phone')
        Skills = request.POST.get('skills')
        Resume = request.FILES.get('resume')

        if Resume is None:
            return render(request, 'uploadresume.html', {'error_message': 'Please upload a PDF, DOC, or DOCX resume.'})

        if not is_allowed_resume_file(Resume):
            return render(request, 'uploadresume.html', {'error_message': 'Only PDF, DOC, or DOCX resumes are allowed.'})

        if Resume.size > MAX_RESUME_SIZE:
            return render(request, 'uploadresume.html', {'error_message': 'Resume size must be 2 MB or less.'})

        user.name = Name
        user.email = Email
        user.phone = Phone
        user.skills = Skills
        user.resume = Resume
        user.save()
        return redirect('showprofile')

    return HttpResponse("Invalid request")
        

def showprofile(request):
    current_user = get_logged_in_jobseeker(request)
    if not current_user:
        return access_denied(request)

    user = JobSeeker.objects.filter(seekerid=current_user.seekerid)
    user_mapped={"username":user}
    return render(request, 'showprofile.html',user_mapped)

def deleteprofile(request, seekerid):
    current_user = get_logged_in_jobseeker(request)
    if not current_user or str(seekerid) != str(current_user.seekerid):
        return access_denied(request)

    profile = JobSeeker.objects.filter(seekerid=current_user.seekerid).first()
    if not profile:
        return access_denied(request)

    profile.delete()
    request.session.flush()
    return redirect('home')
    

def searchprofile(request):
    current_user = get_logged_in_jobseeker(request)
    if not current_user:
        return access_denied(request)

    return render(request, 'searchprofile.html')

def searchprofileprocess(request):
    current_user = get_logged_in_jobseeker(request)
    if not current_user:
        return access_denied(request)

    seeker_id = request.POST.get('seekerid') or request.POST.get('seeker_id')
    email = request.POST.get('email')
    user = JobSeeker.objects.filter(seekerid=current_user.seekerid, email=email)
    user_mapped = {"username": user}
    return render(request, 'showprofile.html', user_mapped)
def modifyprofile(request):
    current_user = get_logged_in_jobseeker(request)
    if not current_user:
        return access_denied(request)

    seekerid = request.GET.get('seekerid')

    if seekerid and str(seekerid) != str(current_user.seekerid):
        return access_denied(request)

    profile = JobSeeker.objects.filter(seekerid=current_user.seekerid).first()
    if not profile:
        return access_denied(request)

    return render(request, 'modifyprofile.html', {'profile': profile})

def modifyprofileprocess(request):

    if request.method == "POST":
        current_user = get_logged_in_jobseeker(request)
        if not current_user:
            return access_denied(request)

        profile = JobSeeker.objects.filter(seekerid=current_user.seekerid).first()
        if not profile:
            return access_denied(request)

        profile.name = request.POST["name"]
        profile.email = request.POST["email"]
        profile.phone = request.POST["phone"]
        profile.skills = request.POST["skills"]

        if request.FILES.get("resume"):
            resume = request.FILES["resume"]
            if not is_allowed_resume_file(resume) or resume.size > MAX_RESUME_SIZE:
                return render(request, 'modifyprofile.html', {'error_message': 'Only PDF, DOC, or DOCX resumes up to 2 MB are allowed.', 'profile': profile})
            profile.resume = resume

        profile.save()

        return redirect("showprofile")

    else:

        return HttpResponse("Invalid Request")
    

def viewjobs(request):
    jobs = Job.objects.all()
    jobs_mapped = {"jobs": jobs}
    return render(request, 'viewjobs.html', jobs_mapped)


def applyjob(request):
    current_user = get_logged_in_jobseeker(request)
    if not current_user:
        return access_denied(request)

    jobid = request.GET.get('jobid')

    context = {}

    if jobid:
        try:
            job = Job.objects.get(jobid=jobid)
            context = {
                'seekerid': current_user.seekerid,
                'seekername': current_user.name,
                'jobid': job.jobid,
                'jobtitle': job.title,
                'company': job.company,
            }
        except Job.DoesNotExist:
            context = {'msg': 'Job Not Found'}

    return render(request, 'applyjobs.html', context)

def applyjobprocess(request):

    if request.method == "POST":

        current_user = get_logged_in_jobseeker(request)
        if not current_user:
            return access_denied(request)

        jobid = request.POST.get('jobid')

        try:
            job = Job.objects.get(jobid=jobid)

            Application.objects.create(
                seeker=current_user,
                job=job,
                status="Pending"
            )

            return render(
                request,
                'viewapplicationstatus.html',
                {'msg': 'Job Application Submitted Successfully'}
            )

        except Job.DoesNotExist:
            return render(
                request,
                'applyjobs.html',
                {'msg': 'Job Not Found'}
            )

    return render(
        request,
        'applyjobs.html',
        {'msg': 'Invalid Request'}
    )


def viewapplicationstatus(request):
    current_user = get_logged_in_jobseeker(request)
    if not current_user:
        return access_denied(request)

    applications = Application.objects.filter(seeker_id=current_user.seekerid)

    return render(
        request,
        "viewapplicationstatus.html",
        {"applications": applications}
    )



#company
def companylogin(request):
    return render(request, 'Company/companylogin.html')


def companydashboard(request):
    return render(request, 'Company/companyhome.html')


def companylogout(request):
    request.session.flush()
    return redirect('companylogin')


@csrf_exempt
def companyloginprocess(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = company.objects.filter(email=email, password=password).first()
        if user:
            request.session['company_id'] = user.companyid
            request.session['company_name'] = user.companyname
            request.session['company_email'] = user.email
            return redirect('companydashboard')
        return render(request, 'Company/companylogin.html', {'msg': 'Company Login Failed'})

    return render(request, 'Company/companylogin.html')


@csrf_exempt
def companyregisterprocess(request):
    if request.method == 'POST':
        companyname = request.POST.get('companyname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('location')

        if company.objects.filter(email=email).exists():
            return render(request, 'Company/companyregister.html', {'msg': 'Email already registered'})

        company.objects.create(
            companyname=companyname,
            email=email,
            password=password,
            location=location,
        )
        return redirect('companylogin')

    return render(request, 'Company/companyregister.html')


def addjob(request):
    current_company = get_logged_in_company(request)
    if not current_company:
        return access_denied(request)

    return render(request, 'Company/addjobs.html')
def addjobprocess(request):
    current_company = get_logged_in_company(request)
    if not current_company:
        return access_denied(request)

    title = request.POST.get('title')
    location = request.POST.get('location')
    salary = request.POST.get('salary')
    description = request.POST.get('description')
    job = Job(title=title, company=current_company.companyname, location=location, salary=salary, description=description)
    job.save()
    return redirect('showjobs')


def showjobs(request):
    current_company = get_logged_in_company(request)
    if not current_company:
        return access_denied(request)

    jobs = Job.objects.filter(company=current_company.companyname)
    jobs_mapped = {"jobs": jobs}
    return render(request, 'Company/showjobs.html', jobs_mapped)


def deletejob(request):
    current_company = get_logged_in_company(request)
    if not current_company:
        return access_denied(request)

    jobs = Job.objects.filter(company=current_company.companyname)
    jobs_mapped = {"jobs": jobs}
    return render(request, 'Company/deletejobs.html', jobs_mapped)


def deletejobprocess(request):
    if request.method == "POST":
        current_company = get_logged_in_company(request)
        if not current_company:
            return access_denied(request)

        jobid = request.POST.get("jobid")

        job = Job.objects.filter(jobid=jobid, company=current_company.companyname).first()
        if not job:
            return access_denied(request)

        job.delete()
        return redirect("showjobs")

    return render(request, 'Company/deletejobs.html', {'msg': 'Invalid Request'})


def viewapplications(request):
    current_company = get_logged_in_company(request)
    if not current_company:
        return access_denied(request)

    applications = Application.objects.select_related('seeker', 'job').filter(job__company=current_company.companyname)
    applications_mapped = {"applications": applications}
    return render(request, 'Company/viewapplications.html', applications_mapped)


def update_application_status(request, status_value):
    if request.method == "POST":
        current_company = get_logged_in_company(request)
        if not current_company:
            return access_denied(request)

        applicationid = request.POST.get("applicationid")

        application = Application.objects.select_related('job').filter(applicationid=applicationid, job__company=current_company.companyname).first()
        if not application:
            return access_denied(request)

        application.status = status_value
        application.save()

    return redirect("viewapplications")


def acceptapplicationinline(request):
    return update_application_status(request, "Accepted")


def rejectapplicationinline(request):
    return update_application_status(request, "Rejected")


def searchjobs(request):
    current_company = get_logged_in_company(request)
    if not current_company:
        return access_denied(request)

    return render(request, 'Company/searchjobs.html')
def searchjobsprocess(request):
    current_company = get_logged_in_company(request)
    if not current_company:
        return access_denied(request)

    jobid = request.POST.get('jobid')

    jobs=Job.objects.filter(jobid=jobid, company=current_company.companyname)
    jobs_mapped = {"jobs": jobs}
    return render(request, 'Company/showjobs.html', jobs_mapped)

def modifyjob(request):
    current_company = get_logged_in_company(request)
    if not current_company:
        return access_denied(request)

    return render(request, 'Company/modifyjobs.html')


from django.shortcuts import render, redirect
from .models import Job

def modifyjobprocess(request):
    if request.method == "POST":

        jobid = request.POST.get("jobid")

        job = Job.objects.get(jobid=jobid)

        job.title = request.POST.get("text1")
        job.location = request.POST.get("text3")
        job.salary = request.POST.get("text4")
        job.description = request.POST.get("text5")

        job.save()

        return redirect("showjobs")

    return render(request, "Company/modifyjobs.html")