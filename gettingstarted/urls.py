from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.views.generic import RedirectView

admin.autodiscover()

from django.conf import settings
from django.conf.urls.static import static

from mentoring import views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', views.home),
    url(r'^admin/', admin.site.urls),


    url(r'^honorsAdmin/$', views.honors_admin_home),
    url(r'^honorsAdmin/mentors/$', views.honors_admin_mentors),
    url(r'^honorsAdmin/mentees/$', views.honors_admin_mentees),
    url(r'^honorsAdmin/export/$', views.export),


    # Default django stuff
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    url(r'^accounts/$', RedirectView.as_view(url='/')),

    url(r'^thankyoumentor/', views.thank_you_mentor),
    url(r'^thankyoumentee/', views.thank_you_mentee),

    url(r'^newmentor/', views.new_mentor),
    url(r'^newmentee/', views.new_mentee),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
