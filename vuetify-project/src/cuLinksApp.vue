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
    <v-alert v-if="isProviderItemsEmpty" color="cyan-darken-4" density="compact" closable>
      Currently there is no link, please go to the "Links creation" tab to add a new link
    </v-alert>
  </div>
  <v-app>
    <v-container>
      <v-row justify="center">
        <v-col md="3" v-for="(objLink, i) in objLinks" :key="i" cols="auto">
          <v-card>
            <v-toolbar color="cyan-darken-4" flat>
              <v-toolbar-title>
                <h5>Link [[i + 1]]</h5>
              </v-toolbar-title>
              <v-btn @click="openDialog(objLink.id, objLink.title, i + 1, i)" class="ma-2" variant="tonal" icon="$mdiEye" :loading="loadingStates[i]"></v-btn>
              <v-btn class="ma-2" variant="tonal" icon="$mdiDelete" @click="remove(objLink.id)"></v-btn>
            </v-toolbar>
            <v-card-text>
              <v-treeview :items="objLink.data" item-value="id" open-all>
                <template v-slot:prepend="{ item, open }">
                  <v-icon v-if="!item.elemnt_type" icon="$mdiApplicationOutline" color="teal-darken-2"></v-icon>
                  <v-icon color="teal-darken-2" v-else>
                    [[ type_elements[item.elemnt_type] ]]
                  </v-icon>
                </template>
              </v-treeview>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-dialog v-model="dialog.visible" transition="dialog-bottom-transition">


        <v-card class="overflow-auto">
          <v-toolbar color="cyan-darken-4">
            <v-toolbar-title>
              <h5>Link - [[dialog.ivalue]]</h5>
            </v-toolbar-title>
            <template v-slot:append>
              <v-btn icon="$close" variant="text" @click="dialog.visible = false"></v-btn>
            </template>
          </v-toolbar>
          <v-card-text class="bg-surface-bright">
            <!-- data2show: [[dialog.data2show]] -->
            <v-timeline align="start" side="end">
              <v-timeline-item
                v-for="(item, i) in dialog.data2show"
                :key="i"
                size="large"
                dot-color="teal-darken-2"
                fill-dot
              >
                <template v-slot:icon>
                  <v-icon v-if="!item.elemnt_type" icon="$mdiApplicationOutline"></v-icon>
                  <v-icon color="teal-darken-2" v-else>
                    [[ type_elements[item.elemnt_type] ]]
                  </v-icon>
                </template>
                <template v-slot:opposite>
                  <span class="text-h5">[[item.provider]] </span>
                </template>
                <v-card class="elevation-2 mb-4 overflow-auto" v-for="(item2, j) in item.data" :key="j">
                  <v-card-title class="mb-0 pb-0">
                    <v-icon v-if="!item2.Type" icon="$mdiApplicationOutline" class="mr-2" size="small"></v-icon>
                    <v-icon v-else :icon="type_elements[item2.Type]" color="teal-darken-2" class="mr-2" size="small"></v-icon>
                    [[item2.Name]]
                     </v-card-title>
                  <v-card-subtitle v-if="item2.Type" class="mt-n1 mb-2">
                    [[item2.Type]]
                  </v-card-subtitle>
                  <v-card-text class="bg-surface-light">
                    <v-container>
                      <v-row>
                        <div v-for="(value, key) in item2" :key="key" v-if="key !== 'Type' && key !== 'Name'">
                          <div v-if="key !== 'Type' && key !== 'Name'">
                            <v-col md="12" class="pa-1 ma-1" cols="auto">
                              <div v-if="isObject(value)">
                                <strong>[[ key ]]:</strong>
                                <div class="ml-1">
                                  <RecursiveItem :data="value" />
                                </div>
                              </div>
                              <div v-else-if="isHtmlKey(key)"></div>
                              <div v-else>
                                <strong>[[ key ]] :</strong> [[ value ]]
                              </div>
                            </v-col>
                          </div>
                        </div>
                      </v-row>
                      <v-row>
                        <div v-for="(value, key) in item2" :key="key" v-if="key !== 'Type' && key !== 'Name'">
                          <div v-if="key !== 'Type' && key !== 'Name'">

                              <div v-if="isHtmlKey(key)">

                                <v-col md="12" class="pa-1 ma-1">
                                  <v-btn v-if="item.provider !== 'OMERO'" color="teal" prepend-icon="$mdiPlusCircle" @click="openExtraActions(value)" class="ma-2 pa-2">
                                    Additional actions
                                  </v-btn>
                                </v-col>
                                <div v-html="value"></div>
                              </div>


                          </div>
                        </div>
                      </v-row>
                    </v-container>
                  </v-card-text>
                </v-card>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
      </v-dialog>


<!-- Dialog for extra actions -->
<v-dialog v-model="extraDialog.visible" transition="dialog-bottom-transition">

    <v-card class="overflow-auto">
      <v-toolbar color="cyan-darken-4">
        <v-toolbar-title>
          <h5>Extracted Tables</h5>
        </v-toolbar-title>
        <v-btn icon="$close" variant="text" @click="extraDialog.visible = false"></v-btn>
      </v-toolbar>
      <v-card-text class="bg-surface-bright">


        <v-container class="">
          <div class="bg-surface-light position-sticky top-0 pa-1 mt-1 " style="z-index:1;">
          <v-container >
            <v-row dense>
               <v-col md="2">

                <v-radio-group v-model="target_option"
                  inline label="Target Object">
                  <v-radio label="Dataset" value="Dataset" ></v-radio>
                  <v-radio label="Project" value="Project"></v-radio>

                </v-radio-group>
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="selectedObject"
                    :hint="selectedDatasetHint"
                    :items="filteredOptions"
                    :item-title="itemTitleKey"
                    item-value="ID"
                    :label="`Select ${itemTitleKey} for Metadata Population`"
                    persistent-hint
                  >
                  </v-select>
                </v-col>
            </v-row>
          </v-container>
          <div class="pa-2">
            <v-alert
              v-model="succAlert2"
              :text="succMessage2"
              type="success"
              density="compact"
              closable
            ></v-alert>
            <v-alert
              v-model="errorAlert2"
              :text="errorMessage2"
              type="error"
              variant="tonal"
              border="top"
              density="compact"
              closable
            ></v-alert>
          </div>
          </div>

          <!-- Loop through all extracted tables -->
          <div v-for="(table, tableIndex) in extraDialog.tables" :key="tableIndex" class="mb-4">
            <v-btn rounded="xl" color="teal" variant="tonal" @click="sendTable(selectedObject, table)" prepend-icon="$mdiPlusCircle"  class="ma-2 pa-2" :disabled="!selectedObject"> Use this table to populate [[selectedDatasetHint]] </v-btn>

            <v-data-table class="custom-header"
              :headers="table.headers"
              :items="table.items"
              :items-per-page="5"

            >

              <template v-slot:no-data>
                <v-btn color="primary" @click="extraDialog.visible = false">
                  Close
                </v-btn>
              </template>
            </v-data-table>
          </div>
        </v-container>
      </v-card-text>
    </v-card>
  </v-dialog>


    </v-container>
    <div><br><br></div>
    <AppFooter />
  </v-app>




</template>

<style>
>>> .v-dialog {
  overflow-y: visible;

}

.custom-header thead tr th {
  background-color: #f8f9fa;
  color: black;
  font-weight: bold;

}

</style>

<script setup>
import { computed, ref, watch, nextTick } from 'vue'
import { useGoTo } from 'vuetify'
import axios from 'axios'
import RecursiveItem from './components/RecursiveItem.vue'

const goTo = useGoTo()

const selectedObject = ref(null);


const target_option =  ref("Dataset")


const filteredOptions = computed(() => {
  console.log(target_option.value)
  if (target_option.value === "Dataset") {
    const arrayOfDataSets= dialog.value.data2show.filter(item => item.provider === 'OMERO').flatMap(item => item.data).filter(dataItem => dataItem.Type === "Image").map(dataItem => ({ Dataset: dataItem.Dataset, ID: dataItem.DatasetID }))
    const uniqueDatasets = arrayOfDataSets.filter(
      (dataset, index, self) =>
        index === self.findIndex((d) => d.ID === dataset.ID)
    );

    return uniqueDatasets
  }else {
    const arrayOfProjects= dialog.value.data2show.filter(item => item.provider === 'OMERO').flatMap(item => item.data).filter(dataItem => dataItem.Type === "Image").map(dataItem => ({ Project: dataItem.Project, ID: dataItem.ProjectID }))
    const uniqueProjects = arrayOfProjects.filter(
      (project, index, self) =>
        index === self.findIndex((p) => p.ID === project.ID)
    );

    return uniqueProjects

  }

});

const itemTitleKey = computed(() => target_option.value);


const selectedDatasetHint = computed(() => {
  // Get the selected dataset object to show as hint
  const objects = filteredOptions.value.find(d => d.ID === selectedObject.value);
  if (target_option.value === "Dataset") {
    return objects ? `Dataset Name: ${objects.Dataset}, ID: ${objects.ID}` : 'Select a dataset to view details';
  }else{
    return objects ? `Project Name: ${objects.Project}, ID: ${objects.ID}` : 'Select a project to view details';
  }
});

const props = defineProps(["Links", "csrf"])
const csrf = props.csrf
const objLinks = ref(JSON.parse((props.Links).replaceAll(", 'children': []", "").replace(/'/g, '"')))
const loadingStates = ref(Array(objLinks.value.length).fill(false))

const dialog = ref({
  visible: false,
  id: null,
  ivalue: null,
  data2show: null,
})

const succAlert = ref(false)
const errorAlert = ref(false)
const succMessage = ref('')
const errorMessage = ref('')

const succAlert2 = ref(false)
const errorAlert2 = ref(false)
const succMessage2 = ref('')
const errorMessage2 = ref('')

const isProviderItemsEmpty = computed(() => objLinks.value.length === 0)

async function openDialog(id, title, ivalue, index) {
  dialog.value.id = id
  dialog.value.ivalue = ivalue
  await getMetadata(id, index)
  dialog.value.visible = true
}

function sendTable(dataID, table){
  //console.log(dataID)
  //console.log(table.items)
  //console.log(table.headers)
  succAlert2.value = false;
  errorAlert2.value = false;
  const ObjType = target_option.value



  const headers = table.headers;  // Array of header objects
  const items = table.items;      // Array of row data

  const payload = {
    Type:ObjType,
    ID: dataID,
    table: {headers, items}
  };

  // Log the payload for debugging
  console.log("Sending the following JSON payload:", payload);

  // Send the JSON payload to the endpoint
  axios.post('/populateTable/', payload, {
    headers: { 'X-CSRFToken': csrf, 'Content-Type': 'application/json' }
  })
  .then(response => {
    console.log("Data sent successfully:", response.data);
    succMessage2.value = 'The table was successfully populate.';
    succAlert2.value = true;
    errorAlert2.value = false;
    dialog.value.visible = false;

  })
  .catch(error => {
    console.error("Error sending data:", error);
    errorMessage2.value = 'Failed to populate the table.' + error;
    errorAlert2.value = true;
    succAlert2.value = false;

  });


}

function isHtmlKey(key) {
  return key.toLowerCase().includes('html')
}

function isObject(val) {
  return val !== null && typeof val === 'object' && !Array.isArray(val)
}

async function getMetadata(idL, index) {
  loadingStates.value[index] = true
  const getData = { idlink: idL }
  try {
    const response = await axios.get('/getMetadata/', { params: getData })
    loadingStates.value[index] = false
    dialog.value.data2show = response.data.metadata
  } catch (err) {
    loadingStates.value[index] = false
    dialog.value.data2show = [{ provider: "Error in the connection with the data providers.", data: err }]
  }
}

function remove(idToRemove) {
  const postData = { data: idToRemove }
  axios
    .post('/removeLinks/', postData, {
      headers: { 'X-CSRFToken': csrf, 'Content-Type': 'application/json' },
    })
    .then(function (response) {
      const deleted = response.data.deleted
      if (deleted === 'True') {
        objLinks.value = objLinks.value.filter(item => item.id !== idToRemove)
        succMessage.value = 'The item has been removed successfully.'
        succAlert.value = true
        errorAlert.value = false
        nextTick(() => {
          goTo('#start-page', { offset: 0 })
        })
      } else {
        errorMessage.value = 'The item could not be removed due to an error.'
        errorAlert.value = true
        succAlert.value = false
        nextTick(() => {
          goTo('#start-page', { offset: 0 })
        })
      }
    })
    .catch(err => {
      errorMessage.value = 'The item could not be removed due to an error.'
      errorAlert.value = true
      succAlert.value = false
      nextTick(() => {
        goTo('#start-page', { offset: 0 })
      })
    })
}

const type_elements = ref({
  Dataset: "$mdiDatabase",
  Experiment: "$mdiFlask",
  Image: "$mdiImage",
  Project: "$mdiFolderMultipleImage",
  Spectra: "$mdiWaveform",
  other: "$mdiFile"
})


const extraDialog = ref({
  visible: false,
  tables: [], // This will hold the extracted tables
});


watch(() => extraDialog.value.visible, (newValue) => {
  if (!newValue) {
    // Reset selectedObject when extraDialog is closed
    selectedObject.value = null;
  }
});

watch(target_option, (newVal) => {
  selectedObject.value = null; // Reset selectedDatabase to null
});


// Method to get headers from the first row of the table
function getHeaders(table) {
  if (table.length === 0) return [];

  return Object.keys(table[0]).map((key) => ({
    title: key,
    value: key,
  }));
}
// Function to extract tables from value
async function openExtraActions(value) {
  // Assuming 'value' contains the HTML string with tables
  extraDialog.value.tables = extractTablesFromHtml(value);
  //console.log(extraDialog.tables)
  extraDialog.value.visible = true; // Show the dialog
}


function extractTablesFromHtml(html) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');
  const extractedTables = [];
  const tables = doc.querySelectorAll('table');

  tables.forEach((table) => {
    const rows = Array.from(table.querySelectorAll('tr'));
    const headerCells = Array.from(rows[0].querySelectorAll('td, th')); // Assuming headers are in the first row

    // Extract headers for v-data-table
    const headers = headerCells.map(cell => ({
      title: cell.innerText.trim(),
      value: cell.innerText.trim()
    }));

    // Extract data items for v-data-table
    const items = rows.slice(1).map((row) => {
      const cells = Array.from(row.querySelectorAll('td'));
      const rowData = {};
      cells.forEach((cell, index) => {
        const header = headers[index]?.value || `column_${index}`;
        rowData[header] = cell.innerText.trim();
      });
      return rowData;
    });

    extractedTables.push({ headers, items });
  });

  return extractedTables;
}

</script>
