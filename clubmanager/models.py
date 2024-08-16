from django.db import models
from accounts.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from datetime import date


class CreatedUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(
        max_length=254, verbose_name='email address', default='No Known Email')
    phone = models.CharField(
        validators=[CustomUser.phone_regex], max_length=15, default='No Known Number')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Member(models.Model):
    # Registered User
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    # Unregistered User
    created_user = models.OneToOneField(
        CreatedUser, on_delete=models.CASCADE, null=True, blank=True)
    score = models.FloatField(default=0.0)
    ranking = models.FloatField(default=999999)
    ordinal_ranking = models.CharField(max_length=30, default="N/A")

    def clean(self):
        if not self.user and not self.created_user:
            raise ValidationError(
                'A member must have either a user or a created user.')

    def __str__(self):
        if self.user:
            return self.user.username
        elif self.created_user:
            return f'{self.created_user.first_name} {self.created_user.last_name}'
        return 'Unknown Member'


class Game(models.Model):
    # Game Setup
    name = models.CharField(max_length=30, default="")
    type = models.CharField(max_length=30)
    buy_in = models.IntegerField()
    date = models.DateField(default=date.today)
    players = models.ManyToManyField(Member)
    player_buy_ins = models.JSONField(default=dict)

    # Game Results
    player_scores = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.name}{self.date}'


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
            if member.id in new_scores:
                new_score = new_scores[member.id]
                member.score = models.F('score') + new_score
                member.save()

        def ordinal(n):
            suffixes = ["th", "st", "nd", "rd"] + ["th"] * 6
            if 10 <= n % 100 <= 20:
                suffix = "th"
            else:
                suffix = suffixes[n % 10]
            return str(n) + suffix

        members = members.order_by('-score')
        for rank, member in enumerate(members, start=1):
            member.ranking = rank
            member.ordinal_ranking = ordinal(rank)
            member.save()

    @classmethod
    def reset_rankings(cls, club_id):
        club = cls.objects.get(id=club_id)
        members = club.members.all()

        for member in members:
            member.score = 0
            member.ranking = 999999
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
