/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import { loadFonts } from './webfontloader'
import VueTelInput from 'vue-tel-input';
import vue3GoogleLogin from "vue3-google-login"

import vuetify from './vuetify'
import pinia from '../store'
import router from '../router'


const client_id =   `${import.meta.env.VITE_GOOGLE_CLIENT_ID}`
export function registerPlugins (app) {
  loadFonts()
  app
    .use(vue3GoogleLogin, {
      clientId : client_id
    })
    .use(vuetify)
    .use(router)
    .use(pinia)
    .use(VueTelInput)
    // .use(vue3GoogleLogin, {
    //   clientId : client_id
    // })
}
