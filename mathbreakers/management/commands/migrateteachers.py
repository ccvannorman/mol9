from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table

class Command(BaseCommand):
    args = 'None'
    help = 'Initializes the database with the base set of data for lesson plans, problem types, etc.'

    def handle(self, *args, **options):

        for u in User.objects.all():
            if u.profile.teacher_of_classroom is not None:
                if not ClassroomTeacherRel.objects.filter(user=u).exists():
                    ct = ClassroomTeacherRel(user=u, classroom=u.profile.teacher_of_classroom)
                    ct.save()
                    print ct
