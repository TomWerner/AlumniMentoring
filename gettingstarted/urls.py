from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.views.generic import RedirectView

admin.autodiscover()

from django.conf import settings
from django.conf.urls.static import static
import django.contrib.auth.views

from mentoring.views import views
from mentoring.views import honors_admin

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', views.home),
    url(r'^admin/', admin.site.urls),


    url(r'^(?i)honorsAdmin/$', honors_admin.home),
    url(r'^(?i)honorsAdmin/mentors/$', honors_admin.mentors),
    url(r'^(?i)honorsAdmin/mentor/([0-9]+)/view', honors_admin.mentor_detail),
    url(r'^(?i)honorsAdmin/mentor/([0-9]+)/details', honors_admin.mentor_detail_page),
    url(r'^(?i)honorsAdmin/mentor/([0-9]+)/approve', honors_admin.mentor_approve),
    url(r'^(?i)honorsAdmin/mentor/([0-9]+)/deny', honors_admin.mentor_deny),
    url(r'^(?i)honorsAdmin/mentees/$', honors_admin.mentees),
    url(r'^(?i)honorsAdmin/mentee/([0-9]+)/view', honors_admin.mentee_detail),
    url(r'^(?i)honorsAdmin/mentee/([0-9]+)/details', honors_admin.mentee_detail_page),
    url(r'^(?i)honorsAdmin/mentee/([0-9]+)/approve', honors_admin.mentee_approve),
    url(r'^(?i)honorsAdmin/mentee/([0-9]+)/deny', honors_admin.mentee_deny),
    url(r'^(?i)honorsAdmin/mentee/([0-9]+)/getmatches', honors_admin.mentee_get_matches),
    url(r'^(?i)honorsAdmin/mentee/([0-9]+)/getallmatches$', honors_admin.mentee_get_all_matches),
    url(r'^(?i)honorsAdmin/mentee/([0-9]+)/getallmatcheslist', honors_admin.mentee_get_all_matches_list),
    url(r'^(?i)honorsAdmin/createPairing', honors_admin.create_pairing),
    url(r'^(?i)honorsAdmin/endPairing', honors_admin.end_pairing),
    url(r'^(?i)honorsAdmin/feedbacks/([0-9]+)/view/', honors_admin.pairing_feedback),
    url(r'^(?i)honorsAdmin/pairs/$', honors_admin.pairings),
    url(r'^(?i)honorsAdmin/export/$', honors_admin.export),
    url(r'^(?i)honorsAdmin/invite/$', honors_admin.invitations),
    url(r'^(?i)honorsAdmin/send_invite/$', honors_admin.send_invite),
    url(r'^(?i)honorsAdmin/preview_invite/$', honors_admin.preview_invite),


    # Default django stuff
    url(r'^(?i)accounts/logout/$', django.contrib.auth.views.logout),
    url(r'^(?i)accounts/login/$', django.contrib.auth.views.login, {'template_name': 'admin/login.html'}),
    url(r'^(?i)accounts/$', RedirectView.as_view(url='/')),

    url(r'^(?i)thankyoumentor/', views.thank_you_mentor),
    url(r'^(?i)thankyoumentee/', views.thank_you_mentee),

    url(r'^(?i)newmentor/', views.new_mentor),
    url(r'^(?i)newmentee/', views.new_mentee),

    url(r'^(?i)confirmation/', views.confirm_account),
    url(r'^(?i)feedback/', views.pairing_feedback),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
