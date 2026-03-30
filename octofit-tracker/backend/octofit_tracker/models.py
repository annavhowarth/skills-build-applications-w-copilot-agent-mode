from djongo import models

class Team(models.Model):
	id = models.ObjectIdField(primary_key=True, editable=False)
	name = models.CharField(max_length=100, unique=True)
	description = models.TextField(blank=True)
	def __str__(self):
		return self.name

class User(models.Model):
	id = models.ObjectIdField(primary_key=True, editable=False)
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=100)
	team = models.ForeignKey(Team, related_name='members', on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	def __str__(self):
		return self.username

class Activity(models.Model):
	id = models.ObjectIdField(primary_key=True, editable=False)
	user = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE)
	type = models.CharField(max_length=100)
	duration = models.PositiveIntegerField(help_text='Duration in minutes')
	date = models.DateField()
	def __str__(self):
		return f"{self.type} - {self.user.username}"

class Workout(models.Model):
	id = models.ObjectIdField(primary_key=True, editable=False)
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	suggested_for = models.ManyToManyField(Team, related_name='workouts')
	def __str__(self):
		return self.name

class Leaderboard(models.Model):
	id = models.ObjectIdField(primary_key=True, editable=False)
	team = models.ForeignKey(Team, related_name='leaderboards', on_delete=models.CASCADE)
	points = models.PositiveIntegerField(default=0)
	def __str__(self):
		return f"{self.team.name} - {self.points} pts"
