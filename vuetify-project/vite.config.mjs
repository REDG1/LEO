// Plugins
import Components from 'unplugin-vue-components/vite'
import Vue from '@vitejs/plugin-vue'
import Vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'
import ViteFonts from 'unplugin-fonts/vite'

// Utilities
import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'
import {resolve} from 'path'


// https://vitejs.dev/config/
export default defineConfig({

  plugins: [
    Vue({
      template: { transformAssetUrls,
       compilerOptions: {
          delimiters : ["[[", "]]"],
        }
       },

    }),
    // https://github.com/vuetifyjs/vuetify-loader/tree/master/packages/vite-plugin#readme
    Vuetify(),
    Components(),
    ViteFonts(),
  ],
  define: { 'process.env': {} },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
    extensions: [
      '.js',
      '.json',
      '.jsx',
      '.mjs',
      '.ts',
      '.tsx',
      '.vue',
    ],
  },
  server: {
    port: 3000,
  },
  build: {
    rollupOptions: {
        input: {
            main: resolve('./src/main.js'),
            currentLinks: resolve('./src/currentLinks.js'),
            settings: resolve('./src/settings.js'),
        },
        output: {
            dir: '../main/static/vue/',
            entryFileNames: '[name].js',
        },
    }
  }
})
