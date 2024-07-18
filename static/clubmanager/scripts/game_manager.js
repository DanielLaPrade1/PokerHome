// Timer
let timer;
let hours = 0;
let minutes = 0;
let seconds = 0;

const timeShown = document.getElementById('timer');
const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');


function startTimer() {
  loadTimerState()
  timer = setInterval(updateTimer, 1000);
  startBtn.hidden = true;
  pauseBtn.hidden = false;
  sessionStorage.setItem('timerRunning', true);
}

function pauseTimer() {
  loadTimerState()
  clearInterval(timer);
  startBtn.hidden = false;
  pauseBtn.hidden = true;
  sessionStorage.setItem('timerRunning', false);
}

function updateTimer() {
  seconds++;
  if (seconds === 60) {
      seconds = 0;
      minutes++;
      if (minutes === 60) {
          minutes = 0;
          hours++;
      }
  }
  updateTimerDisplay()
}

function updateTimerDisplay() {
  function padNumber(number) {
    return number.toString().padStart(2, '0');
  }
  const formattedTime = 
      padNumber(hours) + ':' + 
      padNumber(minutes) + ':' + 
      padNumber(seconds);
  timeShown.textContent = formattedTime;
  // Save Timer State
  sessionStorage.setItem('timerState', JSON.stringify({ hours, minutes, seconds }));
}

function loadTimerState() {
  const elapsedTime = sessionStorage.getItem('timerState');
  if (elapsedTime) {
      const { hours: savedHours, minutes: savedMinutes, seconds: savedSeconds } = JSON.parse(elapsedTime);
      hours = savedHours;
      minutes = savedMinutes;
      seconds = savedSeconds;
      updateTimerDisplay()
  }
}

document.addEventListener('DOMContentLoaded', function() {
  startBtn.addEventListener('click', startTimer);
  pauseBtn.addEventListener('click', pauseTimer);

  // New Game Created, Reset Timer
  const navEntry = performance.getEntriesByType('navigation')[0];
  if (navEntry.type === 'navigate' && navEntry.redirectCount > 0) {
    sessionStorage.removeItem('timerState');
    sessionStorage.removeItem('timerRunning');
  }

  timerRunning = sessionStorage.getItem('timerRunning');
  timer = sessionStorage.getItem('timerState') || null;
  timerRunning == 'true' || timer == null ? startTimer() : pauseTimer();
  
  const form = document.getElementById('input-form');
  // Timer State Handling
  form.addEventListener('submit', () => {
    sessionStorage.removeItem('timerState');
  })
})

//MODALS

// Player Results Modal
const inputResultModal = document.getElementById('input-modal')
timerRunning = sessionStorage.getItem('timerRunning');

// Open Modal
const openInputModal = document.getElementById('open-input-results')
openInputModal.addEventListener('click', () => {
  inputResultModal.showModal()
  inputResultModal.classList.add('active-modal');
  pauseTimer()
})
// Close Modal
const closeInputModal = document.getElementById('close-input-results')
const closeModal = (modal) => {
  modal.classList.remove('active-modal');
  modal.classList.add('closing-modal');
  setTimeout(() => {
    modal.classList.remove('closing-modal');
    modal.close();
  }, 300);
  if (timerRunning == 'true') {
    startTimer();
  }
}
closeInputModal.addEventListener('click', () => closeModal(inputResultModal));

//Update Buy In Modal
const openBuyInModal = document.getElementById('open-buy-in')

//Open Modal
const buyInModal = document.getElementById("update-buy-in-modal")
openBuyInModal.addEventListener('click', () => {
  buyInModal.showModal()
  buyInModal.classList.add('active-modal');
})
// Close Modal
const closeBuyInModal = document.getElementById('close-buy-in')
closeBuyInModal.addEventListener('click', () => closeModal(buyInModal));

// Escape Key For Modals
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && inputResultModal.open) {
    event.preventDefault()
    closeModal(inputResultModal);
  }
  else if (event.key === 'Escape' && buyInModal.open) {
    event.preventDefault()
    closeModal(buyInModal);
  }
})


// Lost Chip Counter
const form = document.getElementById('input-form');
const lostChips = document.getElementById('total-lost-chips');
const playerScores = form.querySelectorAll('.player-score-box');

buyInObj = JSON.parse(document.getElementById('buy-in').textContent);
totalChips = Object.values(buyInObj).reduce((acc, val) => acc + val, 0);
players = JSON.parse(document.getElementById('players').textContent);
const countLostChips = () => {
  let lost = 0;
  playerScores.forEach(input => {
    const value = parseFloat(input.value) || 0;
    lost += value;
  });
  lostChips.textContent = totalChips - lost
  // Change Color
  lostChips.classList.remove('no-loss', 'moderate-loss', 'severe-loss');
  if ((totalChips - lost) == 0) {
    lostChips.classList.add('no-loss')
  } else if (Math.abs(totalChips - lost) < totalChips / 10) {
    lostChips.classList.add('moderate-loss')
  } else {
    lostChips.classList.add('severe-loss')
  }
}

playerScores.forEach(input => {
  input.addEventListener('input', countLostChips);
});

countLostChips();