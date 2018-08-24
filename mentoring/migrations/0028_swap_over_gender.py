from django.db import migrations, transaction

def move_gender(apps, schema_editor):
    Mentor = apps.get_model('mentoring', 'Mentor')
    for row in Mentor.objects.all():
        row.new_gender = row.get_gender_display()
        row.save()

    Mentee = apps.get_model('mentoring', 'Mentee')
    for row in Mentee.objects.all():
        row.new_gender = row.get_gender_display()
        row.save()

class Migration(migrations.Migration):
    dependencies = [
        ('mentoring', '0027_mentee_new_gender'),
    ]

    operations = [
        migrations.RunPython(move_gender),
    ]