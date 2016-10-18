from django.contrib import admin
from .models import *


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


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    fields = (
        'first_name',
        'last_name',
        'gender',
        'active')
    list_display = ('first_name', 'last_name', 'active')

    inlines = [
        MentorContactInline,
        MentorEducationInline,
        MentorCareerInline
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


@admin.register(Mentee)
class MenteeAdmin(admin.ModelAdmin):
    fields = (
        'first_name',
        'last_name',
        'gender',
        'active')
    list_display = ('first_name', 'last_name', 'active')

    inlines = [
        MenteeContactInline,
        MenteeEducationInline,
    ]
