from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import transaction
import uuid

def gen_id():
    return uuid.uuid4().hex[:24]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Clear existing data gracefully
            for model in [Activity, Workout, Leaderboard, User, Team]:
                objs = model.objects.all()
                for obj in objs:
                    if getattr(obj, 'pk', None):
                        obj.delete()

            # Create teams
            marvel = Team.objects.create(id=gen_id(), name='Marvel')
            dc = Team.objects.create(id=gen_id(), name='DC')

            # Create users
            users = [
                User.objects.create(id=gen_id(), name='Iron Man', email='ironman@marvel.com', team=marvel),
                User.objects.create(id=gen_id(), name='Captain America', email='cap@marvel.com', team=marvel),
                User.objects.create(id=gen_id(), name='Spider-Man', email='spiderman@marvel.com', team=marvel),
                User.objects.create(id=gen_id(), name='Superman', email='superman@dc.com', team=dc),
                User.objects.create(id=gen_id(), name='Batman', email='batman@dc.com', team=dc),
                User.objects.create(id=gen_id(), name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            ]

            # Create activities
            Activity.objects.create(id=gen_id(), user=users[0], type='Running', duration=30, calories=300, date='2025-12-11')
            Activity.objects.create(id=gen_id(), user=users[3], type='Swimming', duration=45, calories=400, date='2025-12-10')

            # Create workouts
            workout1 = Workout.objects.create(id=gen_id(), name='Cardio Blast', description='High intensity cardio workout')
            workout2 = Workout.objects.create(id=gen_id(), name='Strength Training', description='Build muscle strength')
            workout1.suggested_for.set([users[0], users[1], users[3]])
            workout2.suggested_for.set([users[2], users[4], users[5]])

            # Create leaderboard
            Leaderboard.objects.create(id=gen_id(), team=marvel, points=250)
            Leaderboard.objects.create(id=gen_id(), team=dc, points=300)

            self.stdout.write(self.style.SUCCESS('Test data populated successfully!'))
