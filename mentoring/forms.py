from django.contrib.auth.models import User
from django.forms import ModelForm, inlineformset_factory

from mentoring.models import Mentor, MentorContactInformation, MentorEducation, MentorEmployment, \
    MenteeContactInformation, Mentee, MenteeEducation


class MentorForm(ModelForm):
    class Meta:
        model = Mentor
        fields = ['first_name', 'last_name', 'gender']


MentorContactFormSet = inlineformset_factory(Mentor, MentorContactInformation,
                                             fields=(
                                                 'primary_phone', 'secondary_phone',
                                                 'primary_email', 'secondary_email',
                                                 'linkedin_url', 'facebook_url',
                                                 'personal_url', 'street_address',
                                                 'city', 'state',))

MentorEducationFormSet = inlineformset_factory(Mentor, MentorEducation,
                                               fields=('school',
                                                       'degree',
                                                       'graduation_year',
                                                       'major1',
                                                       'major2',
                                                       'minor1',
                                                       'minor2',))

MentorEmploymentFormSet = inlineformset_factory(Mentor, MentorEmployment,
                                                fields=('company',
                                                    'title',
                                                    'description'))


class MenteeForm(ModelForm):
    class Meta:
        model = Mentee
        fields = ['first_name', 'last_name', 'gender']


MenteeContactFormSet = inlineformset_factory(Mentee, MenteeContactInformation,
                                             fields=(
                                                 'primary_phone', 'secondary_phone',
                                                 'primary_email', 'secondary_email',
                                                 'linkedin_url', 'facebook_url',
                                                 'personal_url', 'street_address',
                                                 'city', 'state',))

MenteeEducationFormSet = inlineformset_factory(Mentee, MenteeEducation,
                                               fields=('school',
                                                       'graduation_year',
                                                       'major1',
                                                       'major2',
                                                       'minor1',
                                                       'minor2',))
