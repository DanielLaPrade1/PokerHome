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
  localStorage.setItem('timerRunning', true);
}

function pauseTimer() {
  loadTimerState()
  clearInterval(timer);
  startBtn.hidden = false;
  pauseBtn.hidden = true;
  localStorage.setItem('timerRunning', false);
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
  localStorage.setItem('timerState', JSON.stringify({ hours, minutes, seconds }));
}

function loadTimerState() {
  const elapsedTime = localStorage.getItem('timerState');
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
  timerRunning = localStorage.getItem('timerRunning')
  timerRunning == 'true' ? startTimer() : pauseTimer()
})