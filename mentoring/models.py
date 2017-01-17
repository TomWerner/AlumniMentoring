import datetime

from django.contrib.auth.models import User
from django.db import models

from mentoring.util import generate_confirmation_token

genders = (('m', 'Male'), ('f', 'Female'))
feedback_givers = (('1', 'Mentor'), ('2', 'Mentee'))
degree_options = (('ba', 'Bachelor of Arts'),
                  ('bs', 'Bachelor of Sciences'),
                  ('m', 'Masters'),
                  ('d', 'Ph.D'),
                  ('pd', 'MD Ph.D'),
                  ('md', 'MD')
                  )
mentoring_categories = (
    ('1', 'Choice of Major'),
    ('2', 'Academia or Industry'),
    ('3', 'Resume/CV Critique'),
    ('4', 'Parenting vs Career'),
    ('5', 'Work life balance'),
    ('6', 'Life after Iowa'),
    ('7', 'Study Abroad'),
    ('8', 'International Experience'),
    ('9', 'Fellowships'),
    ('10', 'Goals'),
    ('11', 'Shadowing Opportunities'),
    ('12', 'Grad school applications'),
    ('13', 'Med school applications'),
    ('14', 'Job/Internship search'),
    ('15', 'Networking'),
    ('16', 'Advanced degrees'),
    ('17', 'Workplace issues'),
    ('18', 'Personal Experiences'),
    ('19', 'Gender specific'),
)
communication_options = (
    ('1', 'In Person'),
    ('2', 'Phone'),
    ('3', 'Email'),
    ('4', 'Other'),
)


class Mentor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=genders)
    active = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=50, null=True, blank=True)
    active_until = models.DateTimeField(null=True, blank=True)

    def primary_email(self):
        return self.mentorcontactinformation.primary_email

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        approved = "Approved" if self.approved else "Not Approved"
        return self.full_name() + "(" + approved + ")"

    def email(self):
        return self.mentorcontactinformation.email()

    def phone_number(self):
        return self.mentorcontactinformation.phone_number()

    def mailing_address(self):
        return self.mentorcontactinformation.mailing_address()

    def web_contacts(self):
        return self.mentorcontactinformation.web_contacts()

    def education(self):
        return "\n\n".join([x.display_string() for x in self.mentoreducation_set.all()])

    def employment(self):
        return "\n\n".join([x.display_string() for x in self.mentoremployment_set.all()])

    def preferences(self):
        return self.mentorpreference.display_string()


class Mentee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=genders)
    active = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=50, null=True, blank=True)
    active_until = models.DateTimeField(null=True, blank=True)

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        approved = "Approved" if self.approved else "Not Approved"
        return self.full_name() + "(" + approved + ")"

    def primary_email(self):
        return self.menteecontactinformation.primary_email

    def email(self):
        return self.menteecontactinformation.email()

    def phone_number(self):
        return self.menteecontactinformation.phone_number()

    def mailing_address(self):
        return self.menteecontactinformation.mailing_address()

    def web_contacts(self):
        return self.menteecontactinformation.web_contacts()

    def education(self):
        return "\n\n".join([x.display_string() for x in self.menteeeducation_set.all()])

    def employment(self):
        return "This application does not record mentee employment at this time."

    def preferences(self):
        return self.menteepreference.display_string()

    def has_no_mentor(self):
        pairs = self.mentormenteepairs_set.all()
        return len([x for x in pairs if x.is_active()]) == 0

    def score_mentor(self, mentor):
        score = 0
        score += self._score_mentor_preferences(mentor)
        score += self._score_mentor_education(mentor)

        return score

    def _score_mentor_preferences(self, mentor):
        if self.menteepreference is None:
            return 0
        return self.menteepreference.score_mentor(mentor)

    def _score_mentor_education(self, mentor):
        return sum([x.score_mentor(mentor) for x in self.menteeeducation_set.all()])


class MentorContactInformation(models.Model):
    mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE)
    primary_phone = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20, null=True, blank=True)

    primary_email = models.EmailField()
    secondary_email = models.EmailField(null=True, blank=True)

    linkedin_url = models.CharField(max_length=100, null=True, blank=True)
    facebook_url = models.CharField(max_length=100, null=True, blank=True)
    personal_url = models.CharField(max_length=100, null=True, blank=True)

    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=30)

    def email(self):
        result = self.primary_email
        if self.secondary_email is not None and len(self.secondary_email) > 0:
            result += "\n(" + self.secondary_email + ")"
        return result

    def phone_number(self):
        result = self.primary_phone
        if self.secondary_phone is not None and len(self.secondary_phone) > 0:
            result += "\n(" + self.secondary_phone + ")"
        return result

    def mailing_address(self):
        return self.street_address + "\n" + self.city + " " + self.state

    def web_contacts(self):
        return "LinkedIn: " + self.linkedin_url + "\n" + \
               "Facebook:" + self.facebook_url + "\n" + \
               "Personal: " + self.personal_url


class MenteeContactInformation(models.Model):
    mentee = models.OneToOneField(Mentee, on_delete=models.CASCADE)
    primary_phone = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20, null=True, blank=True)

    primary_email = models.EmailField()
    secondary_email = models.EmailField(null=True, blank=True)

    linkedin_url = models.CharField(max_length=100, null=True, blank=True)
    facebook_url = models.CharField(max_length=100, null=True, blank=True)
    personal_url = models.CharField(max_length=100, null=True, blank=True)

    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=30)

    def email(self):
        result = self.primary_email
        if self.secondary_email is not None and len(self.secondary_email) > 0:
            result += "\n(" + self.secondary_email + ")"
        return result

    def phone_number(self):
        result = self.primary_phone
        if self.secondary_phone is not None and len(self.secondary_phone) > 0:
            result += "\n(" + self.secondary_phone + ")"
        return result

    def mailing_address(self):
        return self.street_address + "\n" + self.city + " " + self.state

    def web_contacts(self):
        return "LinkedIn: " + self.linkedin_url + "\n" + \
               "Facebook:" + self.facebook_url + "\n" + \
               "Personal: " + self.personal_url


class MentorEducation(models.Model):
    mentor = models.ForeignKey(Mentor)
    school = models.CharField(max_length=100)
    major1 = models.CharField(max_length=100)
    major2 = models.CharField(max_length=100, blank=True, null=True)
    minor1 = models.CharField(max_length=100, blank=True, null=True)
    minor2 = models.CharField(max_length=100, blank=True, null=True)
    degree = models.CharField(max_length=3, choices=degree_options)
    graduation_year = models.DateField(null=True, blank=True)

    def display_string(self):
        grad_year = str(self.graduation_year.strftime("%B %Y")) if self.graduation_year else 'Year Unknown'
        return self.school + \
               " (" + self.get_degree_display() + ", " + grad_year + ")\n" + \
               "Major(s): " + ", ".join(x for x in [self.major1, self.major2] if x is not None) + "\n" + \
               "Minor(s): " + ", ".join(x for x in [self.minor1, self.minor2] if x is not None) + "\n"


class MenteeEducation(models.Model):
    mentee = models.ForeignKey(Mentee)
    school = models.CharField(max_length=100)
    major1 = models.CharField(max_length=100)
    major2 = models.CharField(max_length=100, blank=True, null=True)
    minor1 = models.CharField(max_length=100, blank=True, null=True)
    minor2 = models.CharField(max_length=100, blank=True, null=True)
    graduation_year = models.DateField()

    def display_string(self):
        grad_year = str(self.graduation_year.strftime("%B %Y")) if self.graduation_year else 'Not Provided'
        return self.school + \
               " (" + grad_year + ")\n" + \
               "Major(s): " + ", ".join(x for x in [self.major1, self.major2] if x is not None) + "\n" + \
               "Minor(s): " + ", ".join(x for x in [self.minor1, self.minor2] if x is not None) + "\n"

    def score_mentor(self, mentor):
        score = 0
        for education in mentor.mentoreducation_set.all():
            majors = [education.major1, education.major2]
            minors = [education.minor1, education.minor2]

            for major in [self.major1, self.major2]:
                if major and major in majors:
                    score += 100
                if major and major in minors:
                    score += 50
            for minor in [self.minor1, self.minor2]:
                if minor and minor in minors:
                    score += 50
                if minor and minor in minors:
                    score += 25
        return score


class MentorEmployment(models.Model):
    mentor = models.ForeignKey(Mentor)
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def display_string(self):
        return self.title + " at " + self.company


class MentorMenteePairs(models.Model):
    mentor = models.ForeignKey(Mentor)
    mentee = models.ForeignKey(Mentee)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def is_active(self):
        return self.end_date is None or self.end_date > datetime.date.today()

    def __str__(self):
        return str(self.mentor) + " and " + str(self.mentee) + " (" + str(self.start_date) + " to " + str(
            self.end_date) + ")"

    def has_no_filled_out_feedback(self):
        return (self.feedback_set.count() == 0 and not self.is_active()) or \
               (self.feedback_set.count() > 0 and
                len([feedback for feedback in self.feedback_set.all() if feedback.filled_out()]) == 0)


class Feedback(models.Model):
    pairing = models.ForeignKey(MentorMenteePairs, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, null=True, blank=True)
    giver = models.CharField(choices=feedback_givers, max_length=1)

    went_well = models.TextField(max_length=1000, null=True, blank=True)
    went_poorly = models.TextField(max_length=1000, null=True, blank=True)
    other = models.TextField(max_length=1000, null=True, blank=True)

    def giver_name_with_role(self):
        return self.giver_name() + " (" + self.get_giver_display() + ")"

    def get_email_recipient(self):
        if self.giver == '1':
            return self.pairing.mentor.primary_email()
        else:
            return self.pairing.mentee.primary_email()

    def giver_name(self):
        if self.giver == '1':
            return self.pairing.mentor.full_name()
        else:
            return self.pairing.mentee.full_name()

    def filled_out(self):
        return self.went_well or self.went_poorly or self.other

    @staticmethod
    def create_feedback(mentor_mentee_pair, mentee=True):
        if mentee:
            mentee_token = generate_confirmation_token(mentor_mentee_pair.mentee.primary_email())
            result = Feedback(pairing_id=mentor_mentee_pair.id, token=mentee_token, giver='2')
        else:
            mentor_token = generate_confirmation_token(mentor_mentee_pair.mentor.primary_email())
            result = Feedback(pairing_id=mentor_mentee_pair.id, token=mentor_token, giver='1')
        result.save()
        return result


class MenteePreference(models.Model):
    mentee = models.OneToOneField(Mentee, on_delete=models.CASCADE)
    first_choice = models.CharField(max_length=2, choices=mentoring_categories)
    second_choice = models.CharField(max_length=2, choices=mentoring_categories, null=True, blank=True)
    third_choice = models.CharField(max_length=2, choices=mentoring_categories, null=True, blank=True)
    preferred_communication = models.CharField(max_length=1, choices=communication_options)

    def display_string(self):
        choices = []
        if self.first_choice is not None:
            choices.append(self.get_first_choice_display())
        if self.second_choice is not None:
            choices.append(self.get_second_choice_display())
        if self.third_choice is not None:
            choices.append(self.get_third_choice_display())
        return "Would like to get *" + self.get_preferred_communication_display() + "* advice on\n" + \
               "\n".join(str(num + 1) + ".) " + choice for num, choice in zip(range(3), choices))

    def score_mentor(self, mentor):
        mentor_pref = mentor.mentorpreference
        score = 0
        score += (self.preferred_communication == mentor_pref.preferred_communication) * 100

        my_choices = [self.first_choice, self.second_choice, self.third_choice]
        their_choices = [mentor_pref.first_choice, mentor_pref.second_choice, mentor_pref.third_choice]

        for i, my_choice in enumerate(my_choices):
            if my_choice and my_choice in their_choices:
                score += int(100 / (i + 1))   # 100 for first choice, 50 for seocnd, 33 for third
        return score


class MentorPreference(models.Model):
    mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE)
    first_choice = models.CharField(max_length=2, choices=mentoring_categories)
    second_choice = models.CharField(max_length=2, choices=mentoring_categories, null=True, blank=True)
    third_choice = models.CharField(max_length=2, choices=mentoring_categories, null=True, blank=True)
    preferred_communication = models.CharField(max_length=1, choices=communication_options)

    def display_string(self):
        choices = []
        if self.first_choice is not None:
            choices.append(self.get_first_choice_display())
        if self.second_choice is not None:
            choices.append(self.get_second_choice_display())
        if self.third_choice is not None:
            choices.append(self.get_third_choice_display())
        return "Would like to give *" + self.get_preferred_communication_display() + "* advice on\n" + \
               "\n".join(str(num + 1) + ".) " + choice for num, choice in zip(range(3), choices))
