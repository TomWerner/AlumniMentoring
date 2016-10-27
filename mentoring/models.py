from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

genders = (('m', 'Male'), ('f', 'Female'))
degree_options = (('ba', 'Bachelor of Arts'),
                  ('bs', 'Bachelor of Sciences'),
                  ('m', 'Masters'),
                  ('d', 'Ph.D'),
                  ('pd', 'MD Ph.D'),
                  ('md', 'MD')
                  )
mentoring_categories = (
    (1, 'Choice of Major'),
    (2, 'Academia or Industry'),
    (3, 'Resume/CV Critique'),
    (4, 'Parenting vs Career'),
    (5, 'Work life balance'),
    (6, 'Life after Iowa'),
    (7, 'Study Abroad'),
    (8, 'International Experience'),
    (9, 'Fellowships'),
    (10, 'Goals'),
    (11, 'Shadowing Opportunities'),
    (12, 'Grad school applications'),
    (13, 'Med school applications'),
    (14, 'Job/Internship search'),
    (15, 'Networking'),
    (16, 'Advanced degrees'),
    (17, 'Workplace issues'),
    (18, 'Personal Experiences'),
    (19, 'Gender specific'),
)
communication_options = (
    (1, 'In Person'),
    (2, 'Phone'),
    (3, 'Email'),
    (4, 'Other'),
)


class Mentor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=genders)
    active = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)


class Mentee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=genders)
    active = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)


class MentorContactInformation(models.Model):
    mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE)
    primary_phone = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20, null=True, blank=True)

    primary_email = models.EmailField()
    secondary_email = models.EmailField(null=True, blank=True)

    linkedin_url = models.CharField(max_length=100, null=True, blank=True)
    facebook_url = models.CharField(max_length=100, null=True, blank=True)
    personal_url = models.CharField(max_length=100, null=True, blank=True)

    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=30)


class MenteeContactInformation(models.Model):
    mentee = models.OneToOneField(Mentee, on_delete=models.CASCADE)
    primary_phone = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20)

    primary_email = models.EmailField()
    secondary_email = models.EmailField()

    linkedin_url = models.CharField(max_length=100, null=True, blank=True)
    facebook_url = models.CharField(max_length=100, null=True, blank=True)
    personal_url = models.CharField(max_length=100, null=True, blank=True)

    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=30)


class MentorEducation(models.Model):
    mentor = models.ForeignKey(Mentor)
    school = models.CharField(max_length=100)
    major1 = models.CharField(max_length=100)
    major2 = models.CharField(max_length=100, blank=True, null=True)
    minor1 = models.CharField(max_length=100, blank=True, null=True)
    minor2 = models.CharField(max_length=100, blank=True, null=True)
    degree = models.CharField(max_length=3, choices=degree_options)
    graduation_year = models.DateField()


class MenteeEducation(models.Model):
    mentee = models.ForeignKey(Mentee)
    school = models.CharField(max_length=100)
    major1 = models.CharField(max_length=100)
    major2 = models.CharField(max_length=100, blank=True, null=True)
    minor1 = models.CharField(max_length=100, blank=True, null=True)
    minor2 = models.CharField(max_length=100, blank=True, null=True)
    graduation_year = models.DateField()


class MentorEmployment(models.Model):
    mentor = models.ForeignKey(Mentor)
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()


class MentorMenteePairs(models.Model):
    mentor = models.ForeignKey(Mentor)
    mentee = models.ForeignKey(Mentee)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    comments = models.TextField()


class MenteePreference:
    mentee = models.ForeignKey(Mentee)
    first_choice = models.CharField(max_length=1, choices=mentoring_categories)
    second_choice = models.CharField(max_length=1, choices=mentoring_categories)
    third_choice = models.CharField(max_length=1, choices=mentoring_categories)
    preferred_communication = models.CharField(max_length=1, choices=communication_options)










