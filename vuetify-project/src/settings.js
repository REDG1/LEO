/**
 * current_links.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */
import '@mdi/font/css/materialdesignicons.css'

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App3 from './settingsApp.vue'

// Composables

const providerSet = document.getElementById('providerSet').getAttribute('value') || '{}';
const providers = document.getElementById('providers').getAttribute('value') || '{}';
const user = document.getElementById('user').getAttribute('value') || '{}';
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].getAttribute('value') || '';

import { createApp } from 'vue'


const app = createApp(App3, {providerSet: providerSet, providers:providers, user:user,csrf:csrf })

registerPlugins(app)

app.mount('#app')


