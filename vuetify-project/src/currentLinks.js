/**
 * current_links.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */
import '@mdi/font/css/materialdesignicons.css'

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App2 from './cuLinksApp.vue'

// Composables

const Links = document.getElementById('Links').getAttribute('value') || '{}';
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].getAttribute('value') || '';

import { createApp } from 'vue'


const app = createApp(App2, {Links: Links, csrf: csrf})

registerPlugins(app)

app.mount('#app')
