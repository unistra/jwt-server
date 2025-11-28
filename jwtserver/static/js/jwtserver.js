import '../css/jwtserver.css'
import '../css/navbar.css'
import '../css/core_header.css'
import '../css/footer.css'

const sign = document.querySelector('[role="img"]')

const icons = sign.querySelector('.icons')
const jwtText = sign.querySelector('.jwt')

const addHover = () => {
  icons.classList.add('hover')
  jwtText.classList.add('hover')
}
const removeHover = () => {
  icons.classList.remove('hover')
  jwtText.classList.remove('hover')
}

icons.addEventListener('mouseover', addHover)
icons.addEventListener('mouseout', removeHover)

jwtText.addEventListener('mouseover', addHover)
jwtText.addEventListener('mouseout', removeHover)
