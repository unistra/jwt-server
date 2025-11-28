import '../css/home_main.css'
import '../css/home_section.css'
import { codeToHtml } from './shiki'

codeToHtml(
  `
import { createApp } from 'vue';
import App from '@/App.vue';

import { CasAuthentication } from 'vue-cas-authentication';
import { router } from '@/router';

import { axiosInstance } from '@/axios';

const app = createApp(App);

const CasOptions = {
  axios: axiosInstance,
  options: {
    appIsAllAuth: true,
    authCasLogoutUrl: 'cas_authentication_logout',
    hasFreeAPI: false,
    jwtServerUrl: 'https://jwtserver.unistra.fr/api',
    loginRoute: {name: 'login'},
    loginRouteIsInternal: true,
    serverCAS: 'https://cas.unistra.fr',
  },
  router: router,
};

app.use(router);
app.use(CasAuthentication, CasOptions);
app.mount('#app');
`,
).then((html) => {
  console.log()
  document.querySelector('.code > section').innerHTML = html
})

document.querySelectorAll('main .container > section article button').forEach((button) => {
  button.addEventListener('click', async function () {
    await navigator.clipboard.writeText(this.dataset.endpoint)
    const originalText = this.innerHTML
    this.innerHTML = `<span>Copié !</span>`
    setTimeout(() => {
      this.innerHTML = originalText
    }, 2000)
  })
})

document.querySelector('.code button').forEach((button) => {})
