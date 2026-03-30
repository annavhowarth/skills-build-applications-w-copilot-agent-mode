from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import transaction

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):

        with transaction.atomic():
            self.stdout.write(self.style.WARNING('Deleting old data...'))
            # Delete in dependency order
            Activity.objects.all().delete()
            Leaderboard.objects.all().delete()
            Workout.objects.all().delete()
            User.objects.all().delete()
            for team in Team.objects.all():
                if team.id:
                    team.delete()

            self.stdout.write(self.style.SUCCESS('Creating teams...'))
            marvel = Team.objects.create(name='Marvel', description='Team Marvel Superheroes')
            dc = Team.objects.create(name='DC', description='Team DC Superheroes')

            self.stdout.write(self.style.SUCCESS('Creating users...'))
            users = [
                User.objects.create(email='tony@stark.com', username='IronMan', team=marvel),
                User.objects.create(email='steve@rogers.com', username='CaptainAmerica', team=marvel),
                User.objects.create(email='bruce@wayne.com', username='Batman', team=dc),
                User.objects.create(email='clark@kent.com', username='Superman', team=dc),
            ]

            self.stdout.write(self.style.SUCCESS('Creating workouts...'))
            workout1 = Workout.objects.create(name='Super Strength', description='Strength training for heroes')
            workout2 = Workout.objects.create(name='Flight Training', description='Aerial maneuvers')
            workout1.suggested_for.set([marvel, dc])
            workout2.suggested_for.set([marvel, dc])

            self.stdout.write(self.style.SUCCESS('Creating activities...'))
            Activity.objects.create(user=users[0], type='Bench Press', duration=60, date='2026-03-01')
            Activity.objects.create(user=users[1], type='Shield Training', duration=45, date='2026-03-02')
            Activity.objects.create(user=users[2], type='Martial Arts', duration=50, date='2026-03-03')
            Activity.objects.create(user=users[3], type='Flight', duration=70, date='2026-03-04')

            self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
            Leaderboard.objects.create(team=marvel, points=150)
            Leaderboard.objects.create(team=dc, points=120)

            self.stdout.write(self.style.SUCCESS('Database populated with superhero test data!'))
