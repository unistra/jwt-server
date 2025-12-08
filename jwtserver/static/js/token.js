import '../css/token_form.css'

document.querySelector('main section button').addEventListener('click', async function () {
  await navigator.clipboard.writeText(this.parentElement.querySelector('span').innerText)
  const innerHTML = this.innerHTML
  this.innerHTML = '<span>Copié !</span>'
  setTimeout(() => {
    this.innerHTML = innerHTML
  }, 2000)
})

const translateTimestamp = (key, definition) => {
  const timestampElement = document.querySelector(`dt[data-key="${key}"]`)
  if (!timestampElement) return

  if (definition) {
    timestampElement.title = definition
    return
  }

  const timestampDefinition = timestampElement.nextElementSibling
  if (!timestampDefinition) return

  const timestampValue = /"([\d,]+)",/.exec(timestampDefinition.innerText)
  if (!timestampValue) return

  const date = new Date(parseInt(timestampValue[1], 10) * 1000)
  console.log(date)

  timestampDefinition.title = new Intl.DateTimeFormat('fr-FR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(date)
}

translateTimestamp('exp')
translateTimestamp('iat')
translateTimestamp('nbf')

const definitions = {
  alg: 'Algorithme utilisé pour signer le jeton.',
  aud: '"Audience" - Identifiant du ou des destinataires du jeton.',
  exp: "\"Expiration time\" - Date d'expiration du jeton.",
  iat: '"Issued at" - Date de création du jeton.',
  iss: "\"Issuer\" - Identifiant de l'émetteur du jeton.",
  jti: '"JWT ID" - Identifiant unique du jeton.',
  kid: 'Identifiant de la clé utilisée pour signer le jeton.',
  nbf: '"Not before" - Date avant laquelle le jeton n’est pas valide.',
  sub: "\"Subject\" - Identifiant unique de l'utilisateur.",
  typ: 'Type de jeton.',
}
for (const definition in definitions) {
  translateTimestamp(definition, definitions[definition])
}
