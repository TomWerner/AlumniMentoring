from django.forms import ModelForm, inlineformset_factory

from mentoring.models import Mentor, MentorContactInformation, MentorEducation, MentorEmployment, \
    MenteeContactInformation, Mentee, MenteeEducation, MenteePreference, MentorPreference


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
                                                       'minor2',),
                                               help_texts={
                                                   'graduation_year': 'Enter the date in YYYY format'
                                               })

MentorEmploymentFormSet = inlineformset_factory(Mentor, MentorEmployment,
                                                fields=('company',
                                                        'title',
                                                        'description'))


MentorPreferenceFormSet = inlineformset_factory(Mentor, MentorPreference,
                                                fields=('first_choice',
                                                        'second_choice',
                                                        'third_choice',
                                                        'preferred_communication'),
                                                labels={'first_choice':'Primary Mentoring Goal',
                                                        'second_choice': 'Goal 2',
                                                        'third_choice': 'Goal 3',
                                                        'preferred_communication': 'Preferred Communication'})


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
                                                       'minor2',),
                                               help_texts={
                                                   'graduation_year': 'Enter the date in a YYYY format'
                                               })

MenteePreferenceFormSet = inlineformset_factory(Mentee, MenteePreference,
                                                fields=('first_choice',
                                                        'second_choice',
                                                        'third_choice',
                                                        'preferred_communication'),
                                                labels={'first_choice':'Primary Mentoring Goal',
                                                        'second_choice': 'Goal 2',
                                                        'third_choice': 'Goal 3',
                                                        'preferred_communication': 'Preferred Communication'})
