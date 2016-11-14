import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from mentoring.forms import *
from mentoring.models import Mentor, MentorContactInformation


def create_new_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('main.html')
    else:
        form = UserCreationForm()

    return render(request, 'new_mentor.html', {'form': form})


def home(request):
    return render(request, 'mock_honors_page.html')


def thank_you_mentor(request):
    return render(request, "thanks.html", {'message': "Thank you for applying to be an honors mentor!"})


def thank_you_mentee(request):
    return render(request, "thanks.html", {'message': "Thank you for applying to be part of honors mentoring!"})


def new_mentor(request):
    if request.method == 'POST':
        mentor_form = MentorForm(request.POST)
        contact_form = MentorContactFormSet(request.POST)
        employment_form = MentorEmploymentFormSet(request.POST)
        education_form = MentorEducationFormSet(request.POST)
        preference_form = MentorPreferenceFormSet(request.POST)

        if mentor_form.is_valid() and contact_form.is_valid() and employment_form.is_valid() and education_form.is_valid() and preference_form.is_valid():
            mentor = mentor_form.save()
            contact_form.instance = mentor
            contact_form.save()
            employment_form.instance = mentor
            employment_form.save()
            education_form.instance = mentor
            education_form.save()
            preference_form.instance = mentor
            preference_form.save()
            return redirect('/thankyoumentor')

    else:
        mentor_form = MentorForm()
        contact_form = MentorContactFormSet()
        education_form = MentorEducationFormSet()
        employment_form = MentorEmploymentFormSet()
        preference_form = MentorPreferenceFormSet()

    return render(request, 'new_mentor.html', {
        'form': mentor_form,
        'contact_form': contact_form,
        'education_form': education_form,
        'employment_form': employment_form,
        'preference_form': preference_form
    })


def new_mentee(request):
    if request.method == 'POST':
        mentee_form = MenteeForm(request.POST)
        contact_form = MenteeContactFormSet(request.POST)
        education_form = MenteeEducationFormSet(request.POST)
        preference_form = MenteePreferenceFormSet(request.POST)

        if mentee_form.is_valid() and contact_form.is_valid() and education_form.is_valid():
            mentee = mentee_form.save()
            contact_form.instance = mentee
            contact_form.save()
            education_form.instance = mentee
            education_form.save()
            preference_form.instance = mentee
            preference_form.save()
            return redirect('/thankyoumentee')

    else:
        mentee_form = MenteeForm()
        contact_form = MenteeContactFormSet()
        education_form = MenteeEducationFormSet()
        preference_form = MenteePreferenceFormSet()

    return render(request, 'new_mentee.html', {
        'form': mentee_form,
        'contact_form': contact_form,
        'education_form': education_form,
        'preference_form': preference_form
    })


@login_required
def honors_admin_home(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/', status=403)

    num_mentors = Mentor.objects.filter(approved=True).count()
    num_active_mentors = Mentor.objects.filter(approved=True, mentormenteepairs__isnull=False).count()
    num_pending_mentors = Mentor.objects.filter(approved=False).count()

    num_mentees = Mentee.objects.filter(approved=True).count()
    num_active_mentees = Mentee.objects.filter(approved=True, mentormenteepairs__isnull=False).count()
    num_pending_mentees = Mentor.objects.filter(approved=False).count()

    return render(request, 'honors_admin_home.html', {
        'num_mentors': num_mentors,
        'num_active_mentors': num_active_mentors,
        'num_pending_mentors': num_pending_mentors,
        'num_mentees': num_mentees,
        'num_active_mentees': num_active_mentees,
        'num_pending_mentees': num_pending_mentees,
    })


def honors_admin_mentors(request):
    mentors = Mentor.objects.all()
    return render(request, 'honors_admin_mentors.html', {
        'mentors': mentors
    })


def honors_admin_mentees(request):
    mentees = Mentee.objects.all()
    return render(request, 'honors_admin_mentees.html', {
        'mentees': mentees
    })


def export(request):
    response = HttpResponse(content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="mentoring.csv"'

    writer = csv.writer(response)
    writer.writerow(['Mentor/Mentee', 'First Name', 'Last Name', 'Gender', 'Approved', 'Active',
                     'Primary Phone', 'Secondary Phone', 'Primary Email', 'Secondary email', 'Linkedin url',
                     'Facebook url', 'Personal url', 'Street Address', 'City', 'State',
                     ])
    for mentor in Mentor.objects.filter(mentorcontactinformation__isnull=False):
        writer.writerow([
            'Mentor',
            mentor.first_name,
            mentor.last_name,
            mentor.get_gender_display(),
            mentor.approved,
            mentor.active,
            mentor.mentorcontactinformation.primary_phone,
            mentor.mentorcontactinformation.secondary_phone,
            mentor.mentorcontactinformation.primary_email,
            mentor.mentorcontactinformation.secondary_email,
            mentor.mentorcontactinformation.linkedin_url,
            mentor.mentorcontactinformation.facebook_url,
            mentor.mentorcontactinformation.personal_url,
            mentor.mentorcontactinformation.street_address,
            mentor.mentorcontactinformation.city,
            mentor.mentorcontactinformation.state,
        ])
    for mentee in Mentee.objects.filter(menteecontactinformation__isnull=False):
        writer.writerow([
            'Mentee',
            mentee.first_name,
            mentee.last_name,
            mentee.get_gender_display(),
            mentee.approved,
            mentee.active,
            mentee.menteecontactinformation.primary_phone,
            mentee.menteecontactinformation.secondary_phone,
            mentee.menteecontactinformation.primary_email,
            mentee.menteecontactinformation.secondary_email,
            mentee.menteecontactinformation.linkedin_url,
            mentee.menteecontactinformation.facebook_url,
            mentee.menteecontactinformation.personal_url,
            mentee.menteecontactinformation.street_address,
            mentee.menteecontactinformation.city,
            mentee.menteecontactinformation.state,
        ])

    return response