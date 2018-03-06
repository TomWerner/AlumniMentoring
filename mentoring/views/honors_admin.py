import csv
import datetime

import xlwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from mentoring.models import Mentor, Mentee, MentorMenteePairs, Feedback


@login_required
def home(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/', status=403, request=request)

    num_mentors = Mentor.objects.filter(approved=True).count()

    # Mentors can be in multiple pairs - we only want active pairs, and we only want a unique count
    num_active_mentors = len(set(
        Mentor.objects.filter(approved=True, mentormenteepairs__isnull=False,
                              mentormenteepairs__end_date__gt=datetime.date.today()).values_list('id')))
    pending_mentors = Mentor.objects.filter(approved=False, confirmed=True)

    num_mentees = Mentee.objects.filter(approved=True).count()

    # Mentees can be in multiple pairs - we only want active pairs, and we only want a unique count
    num_active_mentees = len(set(
        Mentee.objects.filter(approved=True, mentormenteepairs__isnull=False,
                              mentormenteepairs__end_date__gt=datetime.date.today()).values_list('id')))
    pending_mentees = Mentee.objects.filter(approved=False, confirmed=True)

    pairs = MentorMenteePairs.objects.all()
    num_pairs = len(pairs)
    num_active_pairs = len([x for x in pairs if x.is_active()])

    matchless_mentees = Mentee.objects.filter(approved=True)
    matchless_mentees = [x for x in matchless_mentees if x.has_no_mentor()]

    return render(request, 'admin/honors_admin_home.html', {
        'num_mentors': num_mentors,
        'num_active_mentors': num_active_mentors,
        'num_pending_mentors': len(pending_mentors),
        'num_mentees': num_mentees,
        'num_active_mentees': num_active_mentees,
        'num_pending_mentees': len(pending_mentees),
        'num_pairs': num_pairs,
        'num_active_pairs': num_active_pairs,
        'pending_mentors': pending_mentors,
        'pending_mentees': pending_mentees,
        'matchless_mentees': matchless_mentees,
    })


@login_required
def pairings(request):
    pairings = MentorMenteePairs.objects.all()
    pairings = sorted(pairings, key=lambda x: (x.is_active(), x.end_date, x.start_date, x.id), reverse=True)

    return render(request, 'admin/honors_admin_pairings.html', {
        'pairings': pairings
    })


@login_required
def pairing_feedback(request, pairing_id):
    pairing = get_object_or_404(MentorMenteePairs, pk=pairing_id)
    return JsonResponse({
        'title': 'Feedback',
        'html': render_to_string('partials/feedback_view.html', {'feedbacks': list(pairing.feedback_set.all())})
    })

@login_required
def mentors(request):
    mentors = Mentor.objects.all()
    return render(request, 'admin/honors_admin_mentors.html', {
        'mentors': mentors
    })


@login_required
def mentees(request):
    mentees = Mentee.objects.all()
    return render(request, 'admin/honors_admin_mentees.html', {
        'mentees': mentees
    })


def write_mentor_data(wb, people, people_class, person_type):
    # The main sheet with contact information
    main_sheet_name = person_type + 's'
    ws = wb.add_sheet(main_sheet_name)  # type: xlwt.Worksheet

    ws.write(0, 0, 'First Name')
    ws.write(0, 1, 'Last Name')
    ws.write(0, 2, 'Gender')
    ws.write(0, 3, 'Primary Phone')
    ws.write(0, 4, 'Secondary Phone')
    ws.write(0, 5, 'Primary Email')
    ws.write(0, 6, 'Secondary Email')
    ws.write(0, 7, 'Linkedin Url')
    ws.write(0, 8, 'FacebookUrl')
    ws.write(0, 9, 'Personal Url')
    ws.write(0, 10, 'Street Address')
    ws.write(0, 11, 'City')
    ws.write(0, 12, 'State')

    for row_num, person in enumerate(people):
        ws.write(row_num + 1, 0, person.first_name)
        ws.write(row_num + 1, 1, person.last_name)
        ws.write(row_num + 1, 2, person.get_gender_display())
        ws.write(row_num + 1, 3, person.get_contact_information().primary_phone)
        ws.write(row_num + 1, 4, person.get_contact_information().secondary_phone)
        ws.write(row_num + 1, 5, person.get_contact_information().primary_email)
        ws.write(row_num + 1, 6, person.get_contact_information().secondary_email)
        ws.write(row_num + 1, 7, person.get_contact_information().linkedin_url)
        ws.write(row_num + 1, 8, person.get_contact_information().facebook_url)
        ws.write(row_num + 1, 9, person.get_contact_information().personal_url)
        ws.write(row_num + 1, 10, person.get_contact_information().street_address)
        ws.write(row_num + 1, 11, person.get_contact_information().city)
        ws.write(row_num + 1, 12, person.get_contact_information().state)

    ws = wb.add_sheet(person_type + ' Education')  # type: xlwt.Worksheet
    ws.write(0, 0, person_type)
    for i, header in enumerate(people_class.get_education_headers_as_tuple()):
        ws.write(0, i+1, header)

    row_num = 1
    for person_num, person in enumerate(people):
        for education in person.get_education():
            ws.write(row_num, 0, person.full_name())
            for i, data in enumerate(education.data_as_tuple()):
                ws.write(row_num, i+1, data)
            row_num += 1

    if person_type == 'Mentor':
        ws = wb.add_sheet(person_type + ' Employment')  # type: xlwt.Worksheet
        ws.write(0, 0, 'Mentor')
        ws.write(0, 1, 'Company')
        ws.write(0, 2, 'Title')
        ws.write(0, 3, 'Description')

        row_num = 1
        for person in people:
            for employment in person.get_employment():
                ws.write(row_num, 0, person.full_name())
                ws.write(row_num, 1, employment.company)
                ws.write(row_num, 2, employment.title)
                ws.write(row_num, 3, employment.description)
                row_num += 1


def write_pairing_data(wb, pairs):
    ws = wb.add_sheet('Pairings')  # type: xlwt.Worksheet
    ws.write(0, 0, 'Mentor')
    ws.write(0, 1, 'Mentee')
    ws.write(0, 2, 'Start Date')
    ws.write(0, 3, 'End Date')
    ws.write(0, 4, 'Is Active')
    ws.write(0, 5, 'Mentor Went Well')
    ws.write(0, 6, 'Mentor Went Poorly')
    ws.write(0, 7, 'Mentor Other')
    ws.write(0, 8, 'Mentee Went Well')
    ws.write(0, 9, 'Mentee Went Poorly')
    ws.write(0, 10, 'Mentee Other')
    for i, pairing in enumerate(pairs):
        ws.write(i+1, 0, pairing.mentor.full_name())
        ws.write(i+1, 1, pairing.mentee.full_name())
        ws.write(i+1, 2, pairing.start_date.strftime('%Y-%m-%d'))
        if pairing.end_date is not None:
            ws.write(i+1, 3, pairing.end_date.strftime('%Y-%m-%d'))
        ws.write(i+1, 4, pairing.is_active())

        feedback = pairing.get_mentor_feedback()
        if feedback and feedback.filled_out():
            ws.write(i+1, 5, feedback.went_well)
            ws.write(i+1, 6, feedback.went_poorly)
            ws.write(i+1, 7, feedback.other)

        feedback = pairing.get_mentee_feedback()
        if feedback and feedback.filled_out():
            ws.write(i + 1, 8, feedback.went_well)
            ws.write(i + 1, 9, feedback.went_poorly)
            ws.write(i + 1, 10, feedback.other)



@login_required
def export(request):
    response = HttpResponse(content_type='application/ms-excel')
    filename = 'mentoring_export_' + datetime.date.today().strftime('%Y-%m-%d') + '.xls'
    response['Content-Disposition'] = 'attachment; filename=' + filename
    wb = xlwt.Workbook(encoding='utf-8')

    mentors = Mentor.objects.filter(approved=True)
    mentees = Mentee.objects.filter(approved=True)
    pairs = MentorMenteePairs.objects.all()
    pairs = sorted(pairs, key=lambda x: (x.is_active(), x.end_date, x.start_date, x.id), reverse=True)

    write_mentor_data(wb, mentors, Mentor, 'Mentor')
    write_mentor_data(wb, mentees, Mentee, 'Mentee')
    write_pairing_data(wb, pairs)

    wb.save(response)
    return response


@login_required
def mentee_detail(request, mentee_id):
    mentee = get_object_or_404(Mentee, pk=mentee_id)
    return JsonResponse({
        'title': "Mentee Detail",
        'html': render_to_string('partials/detail_view.html', {'person': mentee})
    })


@login_required
def mentor_detail(request, mentor_id):
    mentor = get_object_or_404(Mentor, pk=mentor_id)
    return JsonResponse({
        'title': "Mentor Detail",
        'html': render_to_string('partials/detail_view.html', {'person': mentor})
    })


@login_required
def mentee_approve(request, mentee_id):
    mentee = get_object_or_404(Mentee, pk=mentee_id)
    mentee.approved = True
    mentee.save()
    return redirect('/honorsAdmin', request=request)


@login_required
def mentee_deny(request, mentee_id):
    mentee = get_object_or_404(Mentee, pk=mentee_id)
    mentee.delete()
    return redirect('/honorsAdmin', request=request)


@login_required
def mentor_approve(request, mentor_id):
    mentor = get_object_or_404(Mentor, pk=mentor_id)
    mentor.approved = True
    mentor.save()
    return redirect('/honorsAdmin', request=request)


@login_required
def mentor_deny(request, mentor_id):
    mentor = get_object_or_404(Mentor, pk=mentor_id)
    mentor.delete()
    return redirect('/honorsAdmin', request=request)


@login_required
def mentee_get_matches(request, mentee_id):
    mentee = get_object_or_404(Mentee, pk=mentee_id)

    mentors = Mentor.objects.filter(approved=True)
    scores = [0 for _ in mentors]

    for i, mentor in enumerate(mentors):
        scores[i] += mentee.score_mentor(mentor)

    mentor_results = sorted(list(zip(scores, mentors)), reverse=True, key=lambda x: x[0])
    mentor_results = mentor_results[0: min(len(mentor_results), 5)]

    return JsonResponse({
        'title': "Mentee Matches (Top %s shown)" % len(mentor_results),
        'modal_width': 1000,
        'html': render_to_string('partials/matches_view.html', {
            'person': mentee,
            'mentor_results': mentor_results,
        }, request=request),
        'modal_footer': """<button type="button" class="btn btn-default" id="see_all_mentors">See All Mentors</button>
<button type="button" class="btn btn-primary" id="use_this_mentor">Use This Mentor</button>"""
    })


@login_required
def mentee_get_all_matches(request, mentee_id):
    matchless_mentees = Mentee.objects.filter(approved=True)
    matchless_mentees = [x for x in matchless_mentees if x.has_no_mentor()]

    mentee = Mentee.objects.filter(pk=mentee_id).first()

    if mentee and mentee.id in [x.id for x in matchless_mentees]:
        matchless_mentees.remove(mentee)
        matchless_mentees = [mentee] + matchless_mentees

    return render(request, 'admin/honors_admin_get_all_matches.html', {
        'matchless_mentees': matchless_mentees
    })


@login_required
def mentee_get_all_matches_list(request, mentee_id):
    mentee = get_object_or_404(Mentee, pk=mentee_id)

    mentors = Mentor.objects.filter(approved=True)
    scores = [0 for _ in mentors]

    for i, mentor in enumerate(mentors):
        scores[i] += mentee.score_mentor(mentor)

    mentor_results = sorted(list(zip(scores, mentors)), reverse=True, key=lambda x: x[0])

    return render(request, 'partials/mentor_list.html', {
        'mentee': mentee,
        'mentor_results': mentor_results
    })


def send_paring_email(mentor, mentee):
    # Send an email to both people
    text = "Hello %s and %s,\n\nWe're happy to inform you that you have been selected " \
           "as a mentor mentee pair as part of the Iowa Honors Mentoring program. " \
           "If you need additional help contacting each other, feel free to contact the honors department." \
           "\n" \
           "Mentor:\n" \
           " - %s\n - %s\n\n" \
           "Mentee:\n" \
           " - %s\n - %s\n\n" \
           "Best of luck with the mentorship!\n" \
           "Iowa Honors Mentoring Program" % (mentor.full_name(), mentee.full_name(),
                                              mentor.full_name(), mentor.primary_email(),
                                              mentee.full_name(), mentee.primary_email())

    from_email = 'Iowa Honors Mentoring <%s>' % settings.EMAIL_HOST_USER
    msg = EmailMultiAlternatives("You've been matched for a mentorship!", text, from_email,
                                 [mentee.primary_email(), mentor.primary_email()])
    msg.attach_alternative(render_to_string('email/basic_email.html', {
        'message': text
    }), "text/html")
    msg.send()


@login_required
def resend_pairing_email(request):
    if 'mentee_id' not in request.GET or 'mentor_id' not in request.GET:
        return HttpResponseRedirect(redirect_to='/honorsAdmin', status=404, request=request)
    mentor = get_object_or_404(Mentor, pk=request.GET['mentor_id'])
    mentee = get_object_or_404(Mentee, pk=request.GET['mentee_id'])

    pair = get_object_or_404(MentorMenteePairs, mentee=mentee, mentor=mentor)

    send_paring_email(mentor, mentee)
    messages.success(request, 'An email has been sent to the pair!')

    return redirect('/honorsAdmin/pairs', request=request)


@login_required
def create_pairing(request):
    if 'mentee_id' not in request.GET or 'mentor_id' not in request.GET:
        return HttpResponseRedirect(redirect_to='/honorsAdmin', status=404, request=request)
    mentor = get_object_or_404(Mentor, pk=request.GET['mentor_id'])
    mentee = get_object_or_404(Mentee, pk=request.GET['mentee_id'])

    pair = MentorMenteePairs(mentee=mentee, mentor=mentor, start_date=datetime.date.today())
    pair.save()

    send_paring_email(mentor, mentee)
    messages.success(request, 'An email has been sent to the pair!')

    return redirect('/honorsAdmin/mentee/0/getallmatches', request=request)


def send_feedback_request(feedback):
    from_email = 'Iowa Honors Mentoring <%s>' % settings.EMAIL_HOST_USER
    to = str(feedback.get_email_recipient())
    survey_link = "http://%s/feedback?id=%s&token=%s" % (settings.CURRENT_HOST, feedback.id, feedback.token)
    message = ("Hello!\n\nOn behalf of Honors, thank you for participating in the mentoring program! "
               "In order to continue to improve our program and pairing criteria, we would like to ask you for "
               "some brief feedback about your pairing!\n\n"
               "Survey link: " + survey_link + "\n\nThank you!")
    msg = EmailMultiAlternatives('Iowa Honors Mentoring Feedback Request', message, from_email, [to])
    msg.attach_alternative(render_to_string('email/basic_email.html', {
        'message': message
    }), "text/html")
    msg.send()


@login_required
def end_pairing(request):
    if 'mentee_id' not in request.GET or 'mentor_id' not in request.GET:
        return HttpResponseRedirect(redirect_to='/honorsAdmin', status=404)
    pair = MentorMenteePairs.objects.filter(mentor_id=request.GET['mentor_id'], mentee_id=request.GET['mentee_id'],
                                            end_date__isnull=True).first()
    if pair is None:
        return HttpResponseRedirect(redirect_to='/honorsAdmin', status=404)
    else:
        pair.end_date = datetime.date.today()
        pair.save()

        send_feedback_request(Feedback.create_feedback(pair, mentee=False))
        send_feedback_request(Feedback.create_feedback(pair, mentee=True))
        messages.success(request, "Feedback requests sent!")

        return redirect('/honorsAdmin/pairs', request=request)


@login_required
def invitations(request):
    return render(request, 'admin/honors_admin_invite.html')


def build_invite_message(base_url, name, role, personal_message):
    message = ''
    if personal_message:
        message += personal_message + "\n\n\n\n"
    message += ('Dear %s,\nOn behalf of the Iowa Honors Mentoring program, we would '
                'like to extend you an invitation to become a %s!\n\nTo apply, please go to '
                'http://%s/new%s\n\nThank you!') % (name, role, base_url, role)
    return message


@login_required
def preview_invite(request):
    personal_message = request.GET.get('personal_message', None)
    role = request.GET.get('role', '')
    name = request.GET.get('name', '')
    email = request.GET.get('email_address', '')

    message = build_invite_message(settings.CURRENT_HOST, name, role, personal_message)
    message = 'To: ' + email + '\nSubject: Iowa Honors Mentoring Invitation\n\n' + message

    return JsonResponse({
        'title': "Invitation Preview",
        'html': render_to_string('email/basic_email.html', {'message': message})
    })


@login_required
def send_invite(request):
    personal_message = request.POST.get('personal_message', None)
    role = request.POST.get('role', '')
    name = request.POST.get('name', '')
    email = request.POST.get('email_address', '')

    message = build_invite_message(settings.CURRENT_HOST, name, role, personal_message)

    from_email = 'Iowa Honors Mentoring <%s>' % settings.EMAIL_HOST_USER
    to = str(email)
    msg = EmailMultiAlternatives('Iowa Honors Mentoring Invitation', message, from_email, [to])
    msg.attach_alternative(render_to_string('email/basic_email.html', {
        'message': message
    }), "text/html")
    msg.send()

    messages.success(request, 'Invitation Sent!')
    return redirect('/honorsAdmin', request=request)


@login_required
def mentee_detail_page(request, person_id):
    person = get_object_or_404(Mentee, pk=person_id)
    pairings = person.mentormenteepairs_set.all()
    pairings = sorted(pairings, key=lambda x: (x.is_active(), x.end_date, x.start_date, x.id), reverse=True)
    return render(request, 'admin/person_detail.html', {'person': person, 'pairings': pairings})


@login_required
def mentor_detail_page(request, person_id):
    person = get_object_or_404(Mentor, pk=person_id)
    pairings = person.mentormenteepairs_set.all()
    pairings = sorted(pairings, key=lambda x: (x.is_active(), x.end_date, x.start_date, x.id), reverse=True)
    return render(request, 'admin/person_detail.html', {'person': person, 'pairings': pairings})