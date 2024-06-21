"""
URL configuration for pokerhome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clubmanager.views import LeagueView, PlayersView, RecentGamesView, StartGameView, TournamentCreatorView, DashboardView, LoginView, LogoutView, CreateClubView
from home.views import LandingPageView
from accounts.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Landing Page
    path('',  LandingPageView.as_view(), name='landing'),
    # Authentication
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('register/', RegisterView, name='register'),
    # Club Creation
    path('create-club/', CreateClubView, name='create_club'),
    # Dashboard
    path('dashboard/<int:club_id>/', DashboardView.as_view(), name='dashboard'),
    path('dashboard/<int:club_id>/league/',  LeagueView, name='league'),
    path('dashboard/<int:club_id>/players/', PlayersView,
         name='players'),
    path('dashboard/<int:club_id>/recent-games/',
         RecentGamesView, name='recent-games'),
    path('dashboard/<int:club_id>/start-game/',
         StartGameView, name='start-game'),
    path('dashboard/<int:club_id>/tournaments/', TournamentCreatorView,
         name='tournament-creator'),
]
