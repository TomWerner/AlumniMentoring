from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.forms import inlineformset_factory
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
