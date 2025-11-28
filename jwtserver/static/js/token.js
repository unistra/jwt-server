import '../css/token_form.css'

document.querySelector('main section button').addEventListener('click', async function () {
  await navigator.clipboard.writeText(this.parentElement.querySelector('span').innerText)
  const innerHTML = this.innerHTML
  this.innerHTML = '<span>Copié !</span>'
  setTimeout(() => {
    this.innerHTML = innerHTML
  }, 2000)
})
