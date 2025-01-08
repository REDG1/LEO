<template>
<div id="start-page">
  <v-alert
    v-model="succAlert"
    :text="succMessage"
    type="success"
    density="compact"
    closable
  ></v-alert>
  <v-alert
    v-model="errorAlert"
    :text="errorMessage"
    type="error"
    variant="tonal"
    border="top"
    density="compact"
    closable
  ></v-alert>
  <v-alert
    v-if="isProviderItemsEmpty"
    type="warning"
    density="compact"
    closable
  >
    In addition to OMERO you need to add a second data provider, please add it and configure it correctly.
  </v-alert>
  </div>
  <v-app>
    <v-sheet class="d-flex align-end flex-column">
      <v-btn color="teal" prepend-icon="$mdiPlusCircle" @click="ADD" class="ma-2 pa-2">Add</v-btn>
    </v-sheet>
    <v-container>
      <v-row justify="center">
        <v-col md=4 v-for="(item, i) in items" :key="i" cols="auto">
          <v-card>
            <v-toolbar color="#0377a1" flat>
              <v-toolbar-title>
                <h5>Data provider </h5>
              </v-toolbar-title>
              <v-btn class="ma-2" @click="remove(item.id)" :disabled="isOmero(item)" variant="tonal" icon="$mdiDelete"></v-btn>
            </v-toolbar>

            <v-card-text>
              <v-form ref="formRef" v-model="formValid" lazy-validation>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        label="Host"
                        variant="outlined"
                        v-model="item.host"
                        :rules="hostRules"
                        required
                        :disabled="isOmero(item)"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12">
                      <v-text-field
                        label="API Key"
                        v-model="item.API_Key"
                        variant="outlined"
                        :disabled="isOmero(item)"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12">
                      <v-select
                        label="provider"
                        :items="providerItems"
                        v-model="item.provider"
                        variant="outlined"
                        hide-details
                        required
                        :disabled="isOmero(item)"
                      ></v-select>
                    </v-col>
                  </v-row>
                </v-container>
              </v-form>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="teal" :disabled="!isFormValid(item) || isOmero(item)" @click="openDialog(item)" variant="flat">Save Changes</v-btn>

              <v-dialog v-model="dialog" max-width="400" persistent>
                <v-card>
                  <v-toolbar color="#0377a1" flat>
                    <v-toolbar-title>Save Changes</v-toolbar-title>
                    <template v-slot:append>
                      <v-btn icon="$close" variant="text" @click="dialog = false"></v-btn>
                    </template>
                  </v-toolbar>

                  <v-card-item>Do you want to save the changes?</v-card-item>

                  <template v-slot:actions>
                    <v-spacer></v-spacer>
                    <v-btn color="red-darken-4" @click="dialog = false" variant="flat">Cancel</v-btn>
                    <v-btn color="teal" @click="saveSettings" variant="flat">Accept</v-btn>
                  </template>
                </v-card>
              </v-dialog>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <AppFooter />
  </v-app>
</template>

<script setup>
import { computed, ref , nextTick  } from 'vue'
import { useGoTo } from 'vuetify'
import axios from 'axios'

const goTo = useGoTo()

const props = defineProps(['providerSet', 'providers', 'user', 'csrf']);

const objProvSet = JSON.parse(props.providerSet.replace(/'/g, '"'));
const objproviders = JSON.parse(props.providers.replace(/'/g, '"'));

const providerItems = ref(objproviders);
const dialog = ref(false);
const items = ref(objProvSet);
const currentItem = ref(null);
const succAlert = ref(false);
const errorAlert = ref(false);
const succMessage = ref('');
const errorMessage = ref('');
const formValid = ref(false);
const csrf = props.csrf;

const isProviderItemsEmpty = computed(() => items.value.length < 2);
//console.log(providerItems.value.length)
let tempCount = 0;

function ADD() {
  const addNewValues = { id: 't-' + tempCount, host: '', API_Key: '', provider: providerItems.value[0] };
  items.value.push(addNewValues);
  tempCount++;
}

function remove(idToRemove) {
  if (idToRemove.startsWith('t-')) {
    items.value = items.value.filter(item => item.id !== idToRemove);
    succMessage.value = 'The item has been removed successfully.';
    succAlert.value = true;
    errorAlert.value = false;
    nextTick(() => {
      goTo('#start-page', { offset: 0 });
    });
  } else {
    const postData = { data: idToRemove };
    axios
      .post('/removeSettings/', postData, {
        headers: { 'X-CSRFToken': csrf, 'Content-Type': 'application/json' },
      })
      .then(function (response) {
        const deleted = response.data.deleted;
        if (deleted === 'True') {
          items.value = items.value.filter(item => item.id !== idToRemove);
          succMessage.value = 'The item has been removed successfully.';
          succAlert.value = true;
          errorAlert.value = false;
          nextTick(() => {
            goTo('#start-page', { offset: 0 });
          });
        } else {
          errorMessage.value = 'The item could not be removed due to an error.';
          errorAlert.value = true;
          succAlert.value = false;
          nextTick(() => {
            goTo('#start-page', { offset: 0 });
          });
        }
      })
      .catch(err => {
        //console.log(err);
        errorMessage.value = 'The item could not be removed due to an error.';
        errorAlert.value = true;
      });
  }
}

function openDialog(item) {
  currentItem.value = item;
  dialog.value = true;
}

function saveSettings() {
  const postData = { data: currentItem.value };
  axios
    .post('/saveSettings/', postData, {
      headers: { 'X-CSRFToken': csrf, 'Content-Type': 'application/json' },
    })
    .then(function (response) {
      errorAlert.value = false;
      succAlert.value = true;
      succMessage.value = 'The settings have been saved successfully.';
      //console.log(response);
      const updatedItem = response.data.saveReg; // Extracting saveReg from the response
      const index = items.value.findIndex(item => item.id === currentItem.value.id);
      if (index !== -1) {
        items.value[index] = { ...items.value[index], ...updatedItem }; // Updating the item
      }

      nextTick(() => {
        goTo('#start-page', { offset: 0 });
      });
    })
    .catch(err => {
      //console.log(err);
      errorMessage.value = 'The settings could not be saved due to an error.';
      errorAlert.value = true;
      succAlert.value = false;
      nextTick(() => {
        goTo('#start-page', { offset: 0 });
      });
    });
  dialog.value = false;
}

function isFormValid(item) {
  const hostValid = hostRules.every(rule => rule(item.host) === true);
  return hostValid;
}

function isOmero(item) {
  return item.provider === 'OMERO';
}

const hostRules = [
  value => {
    if (value) return true;
    return 'You must enter a host';
  },
  value => {
    const regex =
      /^(https?:\/\/)?((([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,})|localhost)(:\d{1,5})?(\/.*)?$/;
    if (regex.test(value)) return true;
    return 'Please include a valid host';
  },
];
</script>

<style>
</style>
