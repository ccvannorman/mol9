from django.core.management.base import BaseCommand, CommandError
from mathbreakers.models import *
from mathbreakers.commoncore import get_cc_table

class Command(BaseCommand):
    args = 'None'
    help = 'Sets num_licenses based on purchase record prices'

    def handle(self, *args, **options):
        # ASSUMES LICENSES ARE $3!
        for up in UserProfile.objects.all():
            up.num_licenses = 0
            up.save()

        for pr in PurchaseRecord.objects.filter(code="teacherpurchase"):
            if pr.user is not None:
                prof = pr.user.profile
                prof.num_licenses += pr.price / 300
                prof.save()

