import datetime
import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.forms.utils import ErrorDict
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from mentoring.forms import *
from mentoring.models import Feedback
from mentoring.util import generate_confirmation_token

logger = logging.getLogger('django')

def home(request):
    return render(request, 'mock_honors_page.html')


def thank_you_mentor(request):
    return render(request, "thanks.html", {
        'message': "Thank you for applying to be an honors mentor!",
        'confirmation_pending': request.GET.get('confirmation_pending', 0)
    })


def thank_you_mentee(request):
    return render(request, "thanks.html", {
        'message': "Thank you for applying to be part of honors mentoring!",
        'confirmation_pending': request.GET.get('confirmation_pending', 0)
    })


def check_form(request, forms):
    error_msg = ""
    for form in forms:
        if not form.is_valid():
            if type(form.errors) == ErrorDict:
                d = [form.errors]
            elif type(form.errors) == list:
                d = form.errors
            else:
                logger.error('Unknown type of error: %s, %s' % (type(form.errors), form.errors))
                raise RuntimeError('Unknown type of error: %s, %s' % (type(form.errors), form.errors))
            for error_dict in d:
                for field_name, message in error_dict.items():
                    error_msg += field_name.replace('_', ' ').capitalize() + ': ' + message[0] + "\n"
    if error_msg:
        logger.error(str(forms[0].data))
    logger.error(error_msg)
    messages.error(request, error_msg)


def new_mentor(request):
    if request.method == 'POST':
        mentor_form = MentorForm(request.POST)
        contact_form = MentorContactFormSet(request.POST)
        employment_form = MentorEmploymentFormSet(request.POST)
        education_form = MentorEducationFormSet(request.POST)
        preference_form = MentorPreferenceFormSet(request.POST, form_kwargs={'empty_permitted': False})
        contact_form[0].empty_permitted = False
        education_form[0].empty_permitted = False
        employment_form[0].empty_permitted = False
        preference_form[0].empty_permitted = False

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

            setup_confirmation(mentor)
            mentor.save()
            return redirect('/thankyoumentor?confirmation_pending=1', request=request)
        else:
            messages.error(request, 'There were errors in your submission. Please correct them and submit again.')
            check_form(request, [mentor_form, contact_form, education_form, preference_form, employment_form])
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


def setup_confirmation(person):
    confirmation_token = generate_confirmation_token(person.email())
    person.confirmed = False
    person.confirmation_token = confirmation_token
    person.active_until = datetime.datetime.utcnow() + datetime.timedelta(days=1)

    subject = "Confirm your Iowa Honors Mentoring account"
    from_email = 'Iowa Honors Mentoring <%s>' % settings.EMAIL_HOST_USER
    to = person.primary_email()

    if isinstance(person, Mentor):
        person_type = 'mentor'
    else:
        person_type = 'mentee'

    text_content = ('Hi ' + person.full_name() + ',\n\nThank you for signing up for the Iowa Honors Mentoring program! '
                    'After confirming your account, an honors administrator will review your account and you will be '
                    'notified of your acceptance to the program.\n\nTo confirm your account click this link:\n\n'
                    'http://' + str(settings.CURRENT_HOST) + '/confirmation?token=' + confirmation_token +
                    '&id=' + str(person.id) + '&type=' + str(person_type))
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(render_to_string('email/basic_email.html', {
        'message': text_content
    }), "text/html")
    msg.send()


def new_mentee(request):
    if request.method == 'POST':
        mentee_form = MenteeForm(request.POST)
        contact_form = MenteeContactFormSet(request.POST)
        education_form = MenteeEducationFormSet(request.POST)
        preference_form = MenteePreferenceFormSet(request.POST)
        contact_form[0].empty_permitted = False
        education_form[0].empty_permitted = False
        preference_form[0].empty_permitted = False

        if mentee_form.is_valid() and contact_form.is_valid() and education_form.is_valid() and preference_form.is_valid():
            mentee = mentee_form.save()
            contact_form.instance = mentee
            contact_form.save()
            education_form.instance = mentee
            education_form.save()
            preference_form.instance = mentee
            preference_form.save()
            try:
                setup_confirmation(mentee)
                mentee.save()
                return redirect('/thankyoumentee?confirmation_pending=1', request=request)
            except:
                messages.error(request, 'Sorry! We are experiencing temporary server issues and the '
                                        'administrator has been contacted. '
                                        'Please try again in 15 minutes.')
        else:
            messages.error(request, 'There were errors in your submission. Please correct them and submit again.')
            check_form(request, [mentee_form, contact_form, education_form, preference_form])
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


def confirm_account(request):
    token = request.GET.get('token', None)
    person_type = request.GET.get('type', None)
    id = request.GET.get('id', None)
    if token and person_type and id:
        person = get_object_or_404(Mentor, pk=id) if person_type == 'mentor' else get_object_or_404(Mentee, pk=id)
        token_matches = (person.confirmation_token == token)
        if token_matches and datetime.datetime.now(
                person.active_until.tzinfo) > person.active_until:  # Too late, resend it
            setup_confirmation(person)
            person.save()
            messages.info(request, 'Your token has expired. A new confirmation email has been sent.')
        elif token_matches:
            person.confirmed = True
            person.save()
        return redirect('/thankyou' + person_type, request=request)
    else:
        return redirect('/', request=request)


def pairing_feedback(request):
    if request.method == 'GET':
        token = request.GET.get('token', None)
        id = request.GET.get('id', None)  # The feedback id

        if token and id:
            feedback = get_object_or_404(Feedback, pk=id, token=token)
            return render(request, 'feedback_form.html', {'id': feedback.id, 'token': feedback.token})
        else:
            return render(request, 'general_feedback.html')
    else:
        went_well = request.POST['went_well']
        been_better= request.POST['been_better']
        other = request.POST['other']
        id = request.POST['id']
        token = request.POST['token']

        feedback = get_object_or_404(Feedback, pk=id, token=token)
        feedback.went_well = went_well
        feedback.went_poorly = been_better
        feedback.other = other
        feedback.save()

        return redirect('/')

