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

        // Page Functions
        storedActiveLink = sessionStorage.getItem('activeLink');

        // LEAGUE
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
          // Leaderboard Download Modal
          const clubName = document.getElementById('clubName').textContent;
          const openDownloadLeaderboard = document.getElementById('openDownloadLeaderboard');
          const modalDownloadLeaderboard = document.getElementById('modalDownloadLeaderboard');
          openDownloadLeaderboard.addEventListener('click', async () => { // Open Modal
            modalDownloadLeaderboard.showModal()
            modalDownloadLeaderboard.classList.add('active-modal');
            await getTable(clubName, 'modalTableEmbed')
          })
          const closeModal = (modal) => { // Close Modal
            modal.classList.remove('active-modal');
            modal.classList.add('closing-modal');
            table = document.getElementById('embeddedTabel')
            setTimeout(() => {
              modal.classList.remove('closing-modal');
              modal.close();
              table.remove()
            }, 300);
          }
          const closeDownloadLeaderboard = document.getElementById('closeDownloadLeaderboard');
          closeDownloadLeaderboard.addEventListener('click', () => closeModal(modalDownloadLeaderboard));
          // Download Table
          const downloadTableButton = document.getElementById('downloadTablePDF');
          downloadTableButton.addEventListener('click', async () => {
            await getTable(clubName, 'modalTableEmbed', true)
          });
          // Escape Key For Modals
          document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && modalDownloadLeaderboard.open) {
              event.preventDefault()
              closeModal(modalDownloadLeaderboard);
            }
          })

        }

        // PLAYERS
        if (storedActiveLink == 'players') {
          const openAddPlayer = document.getElementById('addPlayer');
          const modalAddPlayer = document.getElementById('modalAddPlayer');
          openAddPlayer.addEventListener('click', () => {
            modalAddPlayer.showModal();
            modalAddPlayer.classList.add('active-modal');
          })
          const closeAddPlayer = document.getElementById('closeAddPlayer')
          closeAddPlayer.addEventListener('click', () => {
            modalAddPlayer.close();
            modalAddPlayer.classList.remove('active-modal');
          })
        }

        // TOURNAMENT CREATOR
        if (storedActiveLink == 'tournament') {
          document.querySelectorAll('.expand-btn').forEach(button => {
            button.addEventListener('click', function() {
              const row = this.closest('tr');
              const tournamentId = row.nextElementSibling.id;
              const expandedContent = document.getElementById(tournamentId);
              expandedContent.classList.toggle('hidden-table-row');
              expandedContent.classList.toggle('unhidden-table-row');
              this.classList.toggle('rotated-expand');
            });
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

// Downloading Tables and Images
const getTable = async (clubName, placeToEmbed, download=false) => {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  
  doc.setFontSize(27);
  doc.text(clubName + " - Rankings", pageWidth / 2, 20, {align: "center"})

  // Grab Podium
  const podium = document.getElementById('playerPodium');
  const players = document.querySelectorAll('.podium-player')
  // Change Styles for Image
  players.forEach(player => {
    player.style.color = "rgb(50,50,50)";
    player.style.fontWeight = '600';
  })
  const podiumCanvas = await html2canvas(podium);
  const podiumData = podiumCanvas.toDataURL('image/png');
  // Revert Styles
  players.forEach(player => {
    player.style.color = 'lightgray';
    player.style.fontWeight = '300';
  })

  const podiumHeight = 70;
  const podiumWidth = 80;
  doc.addImage(podiumData, 'PNG', (pageWidth - podiumWidth) / 2, 25, podiumWidth, podiumHeight);

  // Generate the table in the PDF
  doc.autoTable({
    html: '#leaderboardTable',
    startY: podiumHeight + 30,
    theme: 'grid',
    styles: {
      fontSize: 9,
      cellPadding: 2,
      overflow: 'linebreak',
      halign: 'center'
    },
    headStyles: {
      fillColor: [200, 200, 200],
      textColor: 20,
      fontStyle: 'bold'
    },
    alternateRowStyles: {
      fillColor: [245, 245, 245]
    }
  });

  // Save pdf
  if (download) {
    doc.save('member_rankings.pdf');
  } else {
    // Convert to Blob and Iframe
    const pdfBlob = doc.output('blob');
    const pdfUrl = URL.createObjectURL(pdfBlob);
    const iframe = document.createElement('iframe');
    iframe.src = pdfUrl;
    iframe.id = "embeddedTabel"
    iframe.classList.add('embedded-tabel')
    // Append to document
    document.getElementById(placeToEmbed).appendChild(iframe);
  }
}
