/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */
import '@mdi/font/css/materialdesignicons.css'

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables

const dataProviders = document.getElementById('dataProviders').getAttribute('value') || '{}';
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].getAttribute('value') || '';


import { createApp } from 'vue'


const app = createApp(App, {

  dataProviders: dataProviders,
  csrf: csrf

})

registerPlugins(app)

app.mount('#app')
