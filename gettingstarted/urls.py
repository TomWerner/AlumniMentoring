from django.conf.urls import include, url

from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.views.generic import RedirectView

admin.autodiscover()

from django.conf import settings
from django.conf.urls.static import static

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Default django stuff
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    url('^register/', CreateView.as_view(
        template_name='new_user.html',
        form_class=UserCreationForm,
        success_url='/'
    )),
    url(r'^accounts/$', RedirectView.as_view(url='/')),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
