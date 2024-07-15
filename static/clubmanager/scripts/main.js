const navLinks = document.querySelectorAll('.nav-link, .top-link');
const contentBox = document.querySelector('.content-box');
const loadingContainer = document.querySelector('.loading-icon');
const leagueLink = document.getElementById('league')
let storedActiveLink = sessionStorage.getItem('activeLink');

//animations
let podium_animation = true

document.addEventListener('DOMContentLoaded', function() {
  //Active Link Rerouting
  const activeLink = Array.from(navLinks).find(link => {
    return link.id === storedActiveLink;
  });
  if (activeLink) {
    activeLink.classList.add('active');
    activeLink.click()
  } else {
    leagueLink.classList.add('active');
    leagueLink.click()
  }
});


//Single page application loading
navLinks.forEach(function(link) {
  link.addEventListener('click', function(event) {
    event.preventDefault();
    const url = this.href;

    //Loading ring appears
    const loading = setTimeout(() => {
      contentBox.innerHTML = '';
      contentBox.appendChild(loadingContainer);
    }, 1000);
    //Fetch Content
    fetch(url)
      .then(response => response.text())
      .then(data => {
        clearTimeout(loading);
        contentBox.innerHTML = data;
        if (contentBox.contains(loadingContainer)) {
          contentBox.removeChild(loadingContainer);
        }
        //League
        storedActiveLink = sessionStorage.getItem('activeLink');
        if (storedActiveLink == 'league') {
          // Rank Animation
          if (podium_animation) {
            podium_animation = false
            const ranks = document.querySelectorAll('.podium__rank');
            ranks.forEach(rank => rank.classList.add('animate'));
            setTimeout(() => {
              ranks.forEach(rank => {
                rank.classList.remove('animate')
              });
            }, 100);
          }
          // Recent Games Button
          const seeAllGames = document.getElementById('see-all-games');
          const recentGamesLink = document.getElementById('recent-games');
          seeAllGames.addEventListener('click', function(event) {
            recentGamesLink.click();
          });
        }
      })
      .catch(error => console.error('Error:', error));
  });
});

const handleLinkClick = (event) => {
  event.preventDefault();

  const clickedLink = event.currentTarget;
  const url = clickedLink.href;

  navLinks.forEach(link => link.classList.remove('active'));
  // Cash game link brings you to league page
  if (clickedLink.id == 'cash') {
    leagueLink.classList.add('active')
    sessionStorage.setItem('activeLink', 'league');
  }
  else {
    clickedLink.classList.add('active');
    sessionStorage.setItem('activeLink', clickedLink.id);
  }

}

navLinks.forEach(link => {
  link.addEventListener('click', handleLinkClick);
});

//Active Top Link
const cash = document.getElementById('cash');
const tournament = document.getElementById('tournament');
const league = document.getElementById('league');
const players = document.getElementById('players');
const recent_games = document.getElementById('recent-games');
const start_game = document.getElementById('start-game');


const activateTopLink = (name) => {
  if (name == 'cash') {
    cash.classList.add("color-active")
    tournament.classList.remove("color-active")
  }
  if (name == 'tournament') {
    tournament.classList.add("color-active")
    cash.classList.remove("color-active")
  }
}

cash.addEventListener('click', () => activateTopLink('cash'))
tournament.addEventListener('click', () => activateTopLink('tournament'))
league.addEventListener('click', () => activateTopLink('cash'))
players.addEventListener('click', () => activateTopLink('cash'))
recent_games.addEventListener('click', () => activateTopLink('cash'))
start_game.addEventListener('click', () => activateTopLink('cash'))

// Message Disapearing Act
const msg = document.getElementById('message');
setTimeout(function() {
  if (msg) {
    msg.style.display = 'none';
  }
}, 4000);

// Nav Button
const navBtn = document.getElementById('nav-btn');
let closedNav = true;
navBtn.addEventListener('click', () => {
  if (closedNav) {
    navBtn.classList.remove('nav-btn-forward')
    navBtn.classList.add('nav-btn-back')
  } else {
    setTimeout(() => {
      navBtn.classList.remove('nav-btn-back')
      navBtn.classList.add('nav-btn-forward')
    }, 400)
  }
  closedNav = !closedNav
})