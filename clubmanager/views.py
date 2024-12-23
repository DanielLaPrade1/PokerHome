from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.template import loader
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied, ValidationError
from .forms import ClubCreationForm, AddMemberForm, GameForm, GameScoresForm, TournamentForm, GameBuyInEditForm, CreatedMemberForm
from .models import Club, Member, Game, Tournament
from accounts.models import CustomUser
from .tournament import calculate_blind_structure


# Ensures that Nobody but the Club Creator can access the club dashboard
class ClubCreatorCheck:
    def dispatch(self, request, *args, **kwargs):
        club_id = kwargs.get('club_id')
        club = get_object_or_404(Club, id=club_id)
        if request.user != club.created_by:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


# Club Dashboard, handles all POST requests
@method_decorator(login_required, name='dispatch')
class DashboardView(ClubCreatorCheck, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club_id = self.kwargs.get('club_id')
        club = get_object_or_404(Club, id=club_id)
        context['club'] = club
        return context

    def post(self, request, **kwargs):
        club_id = self.kwargs.get('club_id')
        club = get_object_or_404(Club, id=club_id)
        # Adding Players To a Club
        if request.POST.get('form_name') == 'players_add':
            form = AddMemberForm(request.POST)
            if form.is_valid():
                try:
                    username = form.cleaned_data['username']
                    user = CustomUser.objects.filter(username=username).first()
                    if user:
                        if club.members.filter(user=user).exists():
                            raise ValidationError(
                                f"{user.username} is already a member of {club.name}")
                        else:
                            member = Member(user=user)
                            member.save()
                            club.members.add(member)
                            club.save()
                            messages.success(request,
                                             f"Member {user.username} added successfully")
                            club.update_rankings(
                                club_id=club_id, new_scores={})
                    else:
                        raise ValidationError("User does not exist.")
                except ValidationError as e:
                    messages.error(request, e.message)
        if request.POST.get('form_name') == 'created_players_add':
            form = CreatedMemberForm(request.POST)
            if form.is_valid():
                new_created_member = form.save()
                member = Member(created_user=new_created_member)
                member.save()
                club.members.add(member)
                club.update_rankings(
                    club_id=club_id, new_scores={})
                club.save()
        # Deleting Players From a Club
        if request.POST.get('form_name') == 'players_remove':
            form = AddMemberForm(request.POST)
            user_id = request.POST.get('user_id')
            member = get_object_or_404(Member, id=user_id)
            club.members.remove(member)
            # Update Rankings
            club.update_rankings(
                club_id=club_id, new_scores={})
        # Starting a game
        if request.POST.get('form_name') == 'start_game':
            form = GameForm(club, request.POST)
            if form.is_valid():
                try:
                    players = form.cleaned_data['players']
                    if len(players) < 2:
                        raise ValidationError(
                            "A Minimum of 2 Players is Required to Start a Game")
                    else:
                        game = form.save()
                        game.save()
                        return redirect('game-manager', club_id=club_id, game_id=game.id)
                except ValidationError as e:
                    messages.error(request, e.message)
        # Deleting a game
        if request.POST.get('form_name') == 'game_remove':
            form = GameForm(club, request.POST)
            game_id = request.POST.get('game_id')
            game = get_object_or_404(Game, id=game_id)
            # Negate all scores and update rankings
            negated_scores = {int(mem): -score for mem,
                              score in game.player_scores.items()}
            print(negated_scores)
            club.update_rankings(
                club_id=club_id, new_scores=negated_scores)
            club.games.remove(game)
        # Starting a tournament
        if request.POST.get('form_name') == 'start_tournament':
            form = TournamentForm(club, request.POST)
            if form.is_valid():
                tournament = form.save()
                tournament.save()
                tournament.blind_structure = calculate_blind_structure(
                    tournament.players.count(), tournament.starting_stack,
                    tournament.target_duration * 60, tournament.blind_duration,
                    tournament.small_blind)
                tournament.save()
                club.tournaments.add(Tournament.objects.get(id=tournament.id))
        # Deleting a tournament
        if request.POST.get('form_name') == 'tournament_remove':
            form = TournamentForm(club, request.POST)
            tournament_id = request.POST.get('tournament_id')
            tournament = get_object_or_404(Tournament, id=tournament_id)
            club.tournaments.remove(tournament)
        return redirect('dashboard', club_id=club_id)


# Dashboard
@ login_required
def LeagueView(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    template = loader.get_template('dashboard/league.html')
    members = club.members.all().order_by('ranking')
    top_3 = members.order_by(
        'ranking')[:3] if len(members) >= 3 else members
    league_template = template.render(
        {'club': club, 'members': members, 'top_3': top_3}, request)
    return HttpResponse(league_template)


def PlayersView(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    form = AddMemberForm()
    create_member_form = CreatedMemberForm()
    members = club.members.all()

    template = loader.get_template('dashboard/players.html')
    players_template = template.render(
        {'form': form, 'create_member_form': create_member_form, 'club': club, 'members': members}, request)
    return HttpResponse(players_template)


@ login_required
def RecentGamesView(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    template = loader.get_template('dashboard/recent_games.html')
    members = club.members.all()

    recent_games_template = template.render(
        {'club': club, 'members': members}, request)
    return HttpResponse(recent_games_template)


@ login_required
def StartGameView(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    template = loader.get_template('dashboard/start_game.html')
    members = club.members.all()
    form = GameForm(club=club)
    start_game_template = template.render(
        {'form': form, 'club': club, 'members': members}, request)
    return HttpResponse(start_game_template)


@ login_required
def GameManagerView(request, club_id, game_id):
    club = get_object_or_404(Club, id=club_id)
    game = get_object_or_404(Game, id=game_id)
    # Update Player Buy Ins
    if game.player_buy_ins == {}:
        buy_ins = {int(player.id): game.buy_in
                   for player in game.players.all()}
        game.player_buy_ins = buy_ins
        game.save()
    if request.method == 'POST':
        game.player_buy_ins = {
            int(id): buy_in for id, buy_in in game.player_buy_ins.items()}
        game.save()
        # Score Input
        if request.POST.get('form_name') == 'input_scores':
            form = GameScoresForm(request.POST, game=game)
            if form.is_valid():
                scores = {}
                for player_id, score in form.cleaned_data.items():
                    scores[int(player_id)] = score - game.player_buy_ins[int(
                        player_id)]
                game.player_scores = scores
                game.save()
                club.games.add(game)
                club.update_rankings(
                    club_id=club_id, new_scores=game.player_scores)
                club.save()
                return redirect('dashboard', club_id=club_id)
        # Buy-In Update
        elif request.POST.get('form_name') == 'update_buy_in':
            form = GameBuyInEditForm(request.POST, game=game)
            if form.is_valid():
                buy_ins = {}
                for player_id, buy_in in form.cleaned_data.items():
                    buy_ins[int(player_id)] = buy_in
                game.player_buy_ins = buy_ins
                game.save()
                game_scores_form = GameScoresForm(game=game)
                buy_in_form = GameBuyInEditForm(game=game)
                context = {'club': club, 'game': game,
                           'game_scores_form': game_scores_form, 'buy_in_form': buy_in_form}

                return render(request, 'dashboard/game_manager.html', context)
    else:
        game_scores_form = GameScoresForm(game=game)
        buy_in_form = GameBuyInEditForm(game=game)
        context = {'club': club, 'game': game,
                   'game_scores_form': game_scores_form, 'buy_in_form': buy_in_form}
        return render(request, 'dashboard/game_manager.html', context)


@ login_required
def TournamentCreatorView(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    template = loader.get_template('dashboard/tournament_creator.html')
    members = club.members.all()
    form = TournamentForm(club=club)
    if request.POST.get('form_name') == 'start_tournament':
        form = TournamentForm(club, request.POST)
        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.save()
            form.save_m2m()
            template = loader.get_template(
                'dashboard/blind_structure.html')
            tournament_template = template.render(
                {'form': form, 'club': club, 'members': members}, request)
            return HttpResponse(tournament_template)
    tournament_template = template.render(
        {'form': form, 'club': club, 'members': members}, request)
    return HttpResponse(tournament_template)


# Auth
def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # User exists
        if user is not None:
            login(request, user)
            club = Club.objects.filter(created_by=user)
            # Redirect to club creation if not already created
            redirect_page = redirect(
                'dashboard', club_id=club.first().id) if club.exists() else redirect('create_club')
            return redirect_page
        # User doesn't exist
        else:
            error_message = 'Invalid username or password'
            return render(request, 'authentication/login.html', {'error_message': error_message})
    return render(request, 'authentication/login.html')


def LogoutView(request):
    logout(request)
    return redirect('landing')


# Club Creation
@ login_required
def CreateClubView(request):
    if request.method == 'POST':
        form = ClubCreationForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            club.created_by = request.user
            club.save()
            member = Member(user=request.user)
            member.save()
            club.members.add(member)
            return redirect('dashboard', club_id=club.id)
    else:
        form = ClubCreationForm()
        return render(request, 'club/create_club.html', {'form': form})
