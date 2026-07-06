from django.db import models

class JobSeeker(models.Model):
    seekerid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=10)
    skills = models.CharField(max_length=200)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.name
    

class Job(models.Model):
    jobid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    salary = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title
    



    

#company
class company(models.Model):
    companyid = models.AutoField(primary_key=True)
    companyname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.companyname

#application
class Application(models.Model):
    applicationid = models.AutoField(primary_key=True)

    seeker = models.ForeignKey(
        JobSeeker,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    def __str__(self):
        return f"{self.seeker.name} - {self.job.title}"