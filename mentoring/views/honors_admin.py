import csv
import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.conf import settings

from mentoring.models import Mentor, Mentee, MentorMenteePairs


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
    pairings = sorted(pairings, key=lambda x: x.is_active(), reverse=True)

    return render(request, 'admin/honors_admin_pairings.html', {
        'pairings': pairings
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


@login_required
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
    # mentee.save()
    mentee.send_email()
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


@login_required
def create_pairing(request):
    if 'mentee_id' not in request.GET or 'mentor_id' not in request.GET:
        return HttpResponseRedirect(redirect_to='/honorsAdmin', status=404, request=request)
    mentor = get_object_or_404(Mentor, pk=request.GET['mentor_id'])
    mentee = get_object_or_404(Mentee, pk=request.GET['mentee_id'])

    pair = MentorMenteePairs(mentee=mentee, mentor=mentor, start_date=datetime.date.today())
    pair.save()
    return redirect('/honorsAdmin/mentee/0/getallmatches', request=request)


@login_required
def end_pairing(request):
    if 'mentee_id' not in request.GET or 'mentor_id' not in request.GET:
        return HttpResponseRedirect(redirect_to='/honorsAdmin', status=404, request=request)
    pair = MentorMenteePairs.objects.filter(mentor_id=request.GET['mentor_id'], mentee_id=request.GET['mentee_id'],
                                            end_date__isnull=True).first()
    if pair is None:
        return HttpResponseRedirect(redirect_to='/honorsAdmin', status=404, request=request)
    else:
        pair.end_date = datetime.date.today()
        pair.save()
        return redirect('/honorsAdmin/pairs', request=request)


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