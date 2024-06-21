from django.db import models
from accounts.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from datetime import date


class Member(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    ranking = models.FloatField(default=999999)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Game(models.Model):
    # e.g. Hold-em, 7-Card Stud, etc
    type = models.CharField(max_length=30)
    buy_in = models.FloatField()
    date = models.DateField(default=date.today)
    players = models.ManyToManyField(Member)

    def __str__(self):
        return f'{self.type}{self.date}'


class Tournament(models.Model):
    name = models.CharField(max_length=30)
    players = models.ManyToManyField(Member)
    # Tourney Creation Fields
    starting_stack = models.IntegerField()
    small_blind = models.IntegerField()
    target_duration = models.FloatField()
    blind_duration = models.IntegerField()

    # Blind Structure
    blind_structure = models.JSONField(default=list)

    def __str__(self):
        return f'{self.name}'


class Club(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(Member, related_name='club_members')
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='club_manager')
    games = models.ManyToManyField(Game, related_name='club_games')
    tournaments = models.ManyToManyField(
        Tournament, related_name='club_tournaments')

    @classmethod
    def update_rankings(cls, club_id, new_scores):
        club = cls.objects.get(id=club_id)
        members = club.members.all()

        for member in members:
            if str(member.user.username) in new_scores:
                new_score = new_scores[str(member.user.username)]
                member.score = models.F('score') + new_score
                member.save()

        members = members.order_by('-score')
        for rank, member in enumerate(members, start=1):
            member.ranking = rank
            member.save()

    def __str__(self):
        return self.name


@receiver(post_save, sender=Club)
def ensure_one_club_per_user(sender, instance, created, **kwargs):
    if created:
        user = instance.created_by
        if Club.objects.filter(created_by=user).count() > 1:
            instance.delete()
            raise ValidationError("You can only create one club.")
