/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles

import 'vuetify/styles'

// Composables

import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'

//extra
import { mdiShieldStar, mdiCircleOutline, mdiFolderNetwork,mdiHomeVariant, mdiDelete, mdiApplicationOutline, mdiMicroscope,
mdiFolderMultipleImage, mdiImage, mdiFlask,mdiDatabase, mdiWaveform, mdiFile, mdiEye, mdiPlusCircle, mdiGitlab, mdiGithub  } from '@mdi/js'
import { VTreeview } from 'vuetify/labs/VTreeview'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  components: {
    VTreeview,
  },
  theme: {
    defaultTheme: 'light',
  },
  icons: {
    defaultSet: 'mdi',
    aliases: {
      ...aliases,
      starShiled: mdiShieldStar,
      mdiCircleOutline: mdiCircleOutline,
      mdiPlusCircle: mdiPlusCircle,
      mdiFolderNetwork: mdiFolderNetwork,
      mdiHomeVariant: mdiHomeVariant,
      mdiDelete: mdiDelete,
      mdiApplicationOutline : mdiApplicationOutline,
      mdiFolderMultipleImage : mdiFolderMultipleImage,
      mdiImage : mdiImage,
      mdiFlask: mdiFlask,
      mdiDatabase : mdiDatabase,
      mdiWaveform, mdiWaveform,
      mdiFile : mdiFile,
      mdiEye : mdiEye,
      mdiGitlab : mdiGitlab,
      mdiGithub : mdiGithub,
      mdiMicroscope : mdiMicroscope

    },
    sets: {
      mdi
    },
  },
})
