from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table

class Command(BaseCommand):
    args = 'None'
    help = 'Initializes the database with the base set of data for lesson plans, problem types, etc.'

    def handle(self, *args, **options):
        for user in User.objects.all():
            UserProfile.objects.get_or_create(user=user)
        if LessonPlan.objects.count() > 0:
            print "You have lesson plans! They will get messed up if you do this."
            print "Exiting without initializing db."
            return
        else:
            self.cc()


    def cc(self):
        cats, data = get_cc_table()
        CCLessonCategory.objects.all().delete()
        CCLessonGrade.objects.all().delete()
        CCLesson.objects.all().delete()

        db_cats = []

        for c in cats:
            dbc = CCLessonCategory(name=c['name'])
            db_cats.append(dbc)
            dbc.save()

        for g in data:
            dbg = CCLessonGrade(name=g['name'])
            dbg.save()
            catid = 0
            for c in g['data']:
                for lesson in c['data']:
                    try:
                        dblesson = CCLesson(name=lesson['name'],
                            description=lesson['description'],
                            mb=lesson['mathbreakers'], 
                            grade=dbg,
                            category=db_cats[catid])
                        dblesson.save()
                    except:
                        print "FAILED: " + lesson['name']
                catid += 1
