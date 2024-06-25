// Input results modal
const inputResultModal = document.getElementById('input-modal')

const openInputModal = document.getElementById('open-input-results')
openInputModal.addEventListener('click', () => {
  inputResultModal.showModal()
})
const closeInputModal = document.getElementById('close-input-results')
closeInputModal.addEventListener('click', () => {
  inputResultModal.close()
})