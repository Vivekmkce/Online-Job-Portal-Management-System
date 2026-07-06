from django.test import Client, TestCase
from django.urls import reverse

from .models import Job, JobSeeker, company


class UBACSessionTests(TestCase):
	def setUp(self):
		self.client = Client()

		self.seeker = JobSeeker.objects.create(
			name='Alice',
			email='alice@example.com',
			password='pass123',
			phone='1234567890',
			skills='Python',
		)
		self.other_seeker = JobSeeker.objects.create(
			name='Bob',
			email='bob@example.com',
			password='pass123',
			phone='9876543210',
			skills='Django',
		)

		self.company = company.objects.create(
			companyname='Acme',
			email='acme@example.com',
			password='pass123',
			location='NY',
		)
		self.other_company = company.objects.create(
			companyname='BetaCorp',
			email='beta@example.com',
			password='pass123',
			location='SF',
		)

		self.owned_job = Job.objects.create(
			title='Developer',
			company=self.company.companyname,
			location='Remote',
			salary=90000,
			description='Build things',
		)
		self.foreign_job = Job.objects.create(
			title='Analyst',
			company=self.other_company.companyname,
			location='Remote',
			salary=80000,
			description='Analyze things',
		)

	def login_seeker(self, seeker):
		session = self.client.session
		session['jobseeker_id'] = seeker.seekerid
		session['jobseeker_name'] = seeker.name
		session['jobseeker_email'] = seeker.email
		session.save()

	def login_company(self, company_user):
		session = self.client.session
		session['company_id'] = company_user.companyid
		session['company_name'] = company_user.companyname
		session['company_email'] = company_user.email
		session.save()

	def test_jobseeker_can_open_own_profile_editor(self):
		self.login_seeker(self.seeker)

		response = self.client.get(
			reverse('modifyprofile'),
			{'seekerid': self.seeker.seekerid},
		)

		self.assertEqual(response.status_code, 200)
		self.assertNotIn(b'Access Denied', response.content)

	def test_jobseeker_cannot_open_other_profile(self):
		self.login_seeker(self.seeker)

		response = self.client.get(
			reverse('modifyprofile'),
			{'seekerid': self.other_seeker.seekerid},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Access Denied')

	def test_company_cannot_delete_foreign_job(self):
		self.login_company(self.company)

		response = self.client.post(
			reverse('deletejobprocess'),
			{'jobid': self.foreign_job.jobid},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Access Denied')
		self.assertTrue(Job.objects.filter(jobid=self.foreign_job.jobid).exists())
