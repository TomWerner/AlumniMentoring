from django.contrib import admin
from .models import *


class MentorMenteePairInline(admin.TabularInline):
    model = MentorMenteePairs
    fields = (
        'mentor',
        'mentee',
        'start_date',
        'end_date',
        'comments'
    )


class MentorContactInline(admin.StackedInline):
    model = MentorContactInformation
    fieldsets = (
        ('Email', {'fields': ('primary_email', 'secondary_email')}),
        ('Phone', {'fields': ('primary_phone', 'secondary_phone')}),
        ('Web Contact', {'fields': ('linkedin_url', 'facebook_url', 'personal_url')}),
        ('Address', {'fields': ('street_address', 'city', 'state')}),
    )


class MentorEducationInline(admin.TabularInline):
    model = MentorEducation
    extra = 1
    fields = (
        'school',
        'major1',
        'major2',
        'minor1',
        'minor2',
        'degree',
        'graduation_year'
    )


class MentorCareerInline(admin.TabularInline):
    model = MentorEmployment
    extra = 1
    fields = (
        'company',
        'title',
        'description'
    )


class MentorPreferenceInline(admin.TabularInline):
    model = MentorPreference
    fields = (
        'first_choice',
        'second_choice',
        'third_choice',
        'preferred_communication'
    )


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    fields = (
        'first_name',
        'last_name',
        'gender',
        'active',
        'approved',
        'confirmed',
        'confirmation_token',
        'active_until',
    )
    list_display = ('first_name', 'last_name', 'active')

    inlines = [
        MentorContactInline,
        MentorEducationInline,
        MentorCareerInline,
        MentorPreferenceInline,
        MentorMenteePairInline,
    ]


class MenteeContactInline(admin.StackedInline):
    model = MenteeContactInformation
    fieldsets = (
        ('Email', {'fields': ('primary_email', 'secondary_email')}),
        ('Phone', {'fields': ('primary_phone', 'secondary_phone')}),
        ('Web Contact', {'fields': ('linkedin_url', 'facebook_url', 'personal_url')}),
        ('Address', {'fields': ('street_address', 'city', 'state')}),
    )


class MenteeEducationInline(admin.TabularInline):
    model = MenteeEducation
    extra = 1
    fields = (
        'school',
        'major1',
        'major2',
        'minor1',
        'minor2',
        'graduation_year'
    )


class MenteePreferenceInline(admin.TabularInline):
    model = MenteePreference
    fields = (
        'first_choice',
        'second_choice',
        'third_choice',
        'preferred_communication'
    )


@admin.register(Mentee)
class MenteeAdmin(admin.ModelAdmin):
    fields = (
        'first_name',
        'last_name',
        'gender',
        'active',
        'approved',
        'confirmed',
        'confirmation_token',
        'active_until',
    )
    list_display = ('first_name', 'last_name', 'active')

    inlines = [
        MenteeContactInline,
        MenteeEducationInline,
        MenteePreferenceInline,
        MentorMenteePairInline,
    ]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    fields = (
        'pairing',
        'token',
        'giver',
        'went_well',
        'went_poorly',
        'other',
    )
    list_display = fields


class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 0
    fields = (
        'giver',
        'went_well',
        'went_poorly',
        'other'
    )


@admin.register(MentorMenteePairs)
class MentorMenteePairsAdmin(admin.ModelAdmin):
    fields = (
        'mentor',
        'mentee',
        'start_date',
        'end_date'
    )
    list_display = fields
    inlines = [
        FeedbackInline
    ]

