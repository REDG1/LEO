<template>
<div id="start-page">
  <v-alert
    v-model= "succAlert"
    text="The link has been saved successfully"
    type="success"
    density="compact"
    closable
  ></v-alert>
  <v-alert
    v-model= "errorAlert"
    text="The link has not been saved due to an error, please try again."
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


    <v-container>
      <v-row justify="center">
        <v-col md=3  v-for="(fCard, i) in fCards" :key="fCard.title+fCard.host" cols="auto">
           <v-card>
              <v-toolbar color = "#0377a1" flat>
                <v-toolbar-title>[[fCard.title]]</v-toolbar-title>
              </v-toolbar>

              <v-card-text >
              <v-card color="#0377a1"
              variant="tonal"
              class="mx-auto my-1 py-1 mx-n2"
                >
                <div  class="text-h6 mx-3">
                  [[ getTitleTable(fCard.element)]]
                </div>

              </v-card>

              <v-data-table

                v-model="selectedItems[`${fCard.title}#domain#${fCard.host}`]"
                items-per-page = 5
                :items=fCard.element
                item-value="title"
                item-key="id"
                :headers =" getHeader(fCard.title, fCard.host)"
                return-object
                show-select
                show-expand
              >

              <template  v-slot:expanded-row="{ columns, item }">
                <tr :id="item.id" v-if="item.children">
                  <td :colspan="columns.length">

                    <v-card color="#0377a1"
                    variant="tonal"
                    class="mx-auto my-1 py-1 mx-n2"
                      >
                        <div class="text-h6 mx-3">
                         [[ getTitleTable(item.children)]]
                        </div>
                      </v-card>


                    <v-data-table-virtual
                      v-model="selectedItems[`${fCard.title}#domain#${fCard.host}`]"
                      :items="item.children"
                      item-value="title"
                      item-key="id"
                      :headers = " getHeader(fCard.title, fCard.host)"
                      return-object
                      show-select
                      show-expand
                    >
                      <template  v-slot:expanded-row="{ columns, item }">
                        <tr v-if="item.children">
                          <td :colspan="columns.length">
                          <v-card color="#0377a1"
                          variant="tonal"
                          class="mx-auto my-1 py-1 mx-n2"
                            >
                              <div class="text-h6 mx-3">
                                 [[ getTitleTable(item.children)]]
                              </div>
                            </v-card>

                            <v-data-table-virtual
                              v-model="selectedItems[`${fCard.title}#domain#${fCard.host}`]"
                              :headers = " getHeader(fCard.title, fCard.host)"
                              :items="item.children"
                              item-value="title"
                              item-key="id"
                              return-object
                              show-select


                            ></v-data-table-virtual>
                          </td>
                        </tr>

                      </template>
                    </v-data-table-virtual>
                  </td>
                </tr>




              </template>

              </v-data-table>



              </v-card-text >
           </v-card>





        </v-col>
      </v-row>



      <v-row align="center" justify="center">
        <v-col >
           <v-card class="mb-8">
              <v-toolbar color="cyan-darken-4" flat>
                <v-toolbar-title>Files to link</v-toolbar-title>
              </v-toolbar>
              <v-card-text >
              <v-row no-gutters >
                <v-col  md=6 v-for="(values, i) in getValues2link" >

                      <v-treeview  item-value="id" :items="[values]" >
                      <template v-slot:prepend="{ item, open }" >

                            <v-icon v-if="!item.types" icon="$mdiApplicationOutline" color="teal-darken-2" ></v-icon>
                            <v-icon color="teal-darken-2" v-else> [[ type_elements[item.types] ]] </v-icon>

                        </template>
                      </v-treeview>

                </v-col>
              </v-row>
              </v-card-text>


              <v-divider></v-divider>

              <v-card-actions>

                <v-spacer></v-spacer>

                <v-dialog v-model="dialog" max-width="400" persistent>
                  <template v-slot:activator="{ props: activatorProps }">
                    <v-btn :disabled="are2Elements" append-icon="$plus" color="teal" text="Save" variant="flat" v-bind="activatorProps"></v-btn>
                  </template>

                  <v-card>

                    <v-toolbar color="cyan-darken-4" flat>
                      <v-toolbar-title>Save Items</v-toolbar-title>
                      <template v-slot:append>
                        <v-btn icon="$close" variant="text" @click="dialog = false"></v-btn>
                      </template>
                    </v-toolbar>

                    <v-card-item>
                    Do you want to link and saved the selected items?

                    </v-card-item>

                    <template v-slot:actions>
                      <v-spacer></v-spacer>

                      <v-btn color="red-darken-4" @click="dialog = false" variant="flat"> Cancel </v-btn>

                      <v-btn color="teal" @click="saveLinks" variant="flat"> Accept </v-btn>
                    </template>
                  </v-card>

             </v-dialog>

              </v-card-actions>
          </v-card>
        </v-col>
      </v-row>


     <AppFooter />
     </v-container>


  </v-app>

</template>



<style>
th {
   display: none;
}


</style>
<script setup>

  import { computed, ref , watch, nextTick  } from 'vue'
  import { useGoTo } from 'vuetify'
  import axios from 'axios'

  const goTo = useGoTo()

  const props = defineProps(["dataProviders", "csrf"]);
  const objDP = JSON.parse((props.dataProviders).replaceAll(", 'children': []", "").replace(/'/g, '"'));

  const csrf = props.csrf;

  function saveLinks(){

    //console.log(getValues2link.value)
    const postData = {data: getValues2link.value}
    axios.post('/saveElementsAndLinks/', postData , {headers :{'X-CSRFToken': csrf, 'Content-Type': 'application/json' }})
    .then(function (response) {
      succAlert.value=true
      errorAlert.value=false
      //console.log(response);
      // Ensure the DOM has updated before scrolling
      nextTick(() => {
        goTo('#start-page', { offset: 0 });
      });
    })
    .catch((err) => {
        //console.log(err);
        errorAlert.value=true
        succAlert.value=false
        // Ensure the DOM has updated before scrolling
      nextTick(() => {
        goTo('#start-page', { offset: 0 });
      });
      })
      .finally(() => {
      dialog.value = false;
    });




  };

  const fCards = ref(objDP);
  const selectedItems =  ref({});

  const isProviderItemsEmpty = computed(() => fCards.value.length < 2);

  function getHeader(title_tab, host_tab){
    //console.log (title_tab+host_tab)
    return [{ title: 'title', value: 'title', key: title_tab+"#domain#"+host_tab },]
  }

  const dialog = ref(false);
  const succAlert = ref(false)
  const errorAlert = ref(false)

  function getTitleTable(elements){

    if (elements.length > 0){

      return elements[0].types
    }else {
      return ""
    }

  }


//validation of the number of elements to be linked
  const are2Elements = computed(()=>{
    const objectLength = Object.keys(selectedItems.value).length;
    let empty = false

    let countElwithObj = 0
    for (const [key, value] of Object.entries(selectedItems.value)) {
      if (value.length == 0){
        countElwithObj = countElwithObj +1;
      }
    }

    if ((objectLength-countElwithObj)< 2){
      empty = true
    }


    if(objectLength > 1 && empty === false){
      return false;
    }else{
      return true;
    }

  })


  function deepEqual(a, b) {
    if (a === b) return true;
    if (typeof a !== "object" || typeof b !== "object") return false;

    const keysA = Object.keys(a);
    const keysB = Object.keys(b);

    if (keysA.length !== keysB.length) return false;

    for (const key of keysA) {
      if (!keysB.includes(key) || !deepEqual(a[key], b[key])) return false;
    }

    return true;
  }

let oldValue = { ...selectedItems }; // Initial shallow copy
  watch(selectedItems, (newValue) => {

   // Log changes for existing keys
    for (const key in newValue) {
      //console.log("keys", key)
      if (newValue[key] !== oldValue[key]) {
        //console.log(`Key: ${key}, New value: ${newValue[key]}, Old value: ${oldValue[key]}`);

      // Ensure values are defined before stringifying
        const newObj = newValue[key] !== undefined ? JSON.parse(JSON.stringify(newValue[key])) : [];
        const oldObj = oldValue[key] !== undefined ? JSON.parse(JSON.stringify(oldValue[key])) : [];

        // Find added or modified items

        const addedOrModified = newObj.filter((newItem) => {
          const oldItem = oldObj.find((item) => item.id === newItem.id);
          return !oldItem || !deepEqual(newItem, oldItem);
        });

      //console.log("Added or modified items of", key, " - ", addedOrModified);
      // Find removed items
      const removed = oldObj.filter((oldItem) => !newValue[key].some((item) => item.id === oldItem.id));

      //console.log("Removed items:", removed);
      const currentProv = objDP.find(obj => obj.title+"#domain#"+obj.host === key);



       //add items
      // Function to add ancestors recursively
      const addAncestors = (item, key) => {
        const parentData = findParentData(item.parent, currentProv["element"]);
        if (parentData) {
          const findParent = selectedItems.value[key].find((el) => el.id === parentData.id);
          if (!findParent) {
            selectedItems.value[key].push(parentData);
            addAncestors(parentData, key); // Recursively add parent's ancestors
          }
        }
      };

      // Recursive function to add descendants
      const addDescendants = (item, key) => {
        if (item.children && item.children.length > 0) {
          for (const child of item.children) {
            const findChild = selectedItems.value[key].find((el) => el.id === child.id);
            if (!findChild) {
              selectedItems.value[key].push(child);
              addDescendants(child, key); // Recursively add child's descendants
            }
          }
        }
      };

      // Helper function to find parent data
      const findParentData = (parentId, elements) => {
        for (const el of elements) {
          if (el.id === parentId) {
            return el;
          }
          if (el.children) {
            const found = findParentData(parentId, el.children);
            if (found) {
              return found;
            }
          }
        }
        return null;
      };

      // Helper function to find item data by id
      const findItemData = (itemId, elements) => {
        for (const el of elements) {
          if (el.id === itemId) {
            return el;
          }
          if (el.children) {
            const found = findItemData(itemId, el.children);
            if (found) {
              return found;
            }
          }
        }
        return null;
      };



      // Add items and their ancestors and descendants
      for (const addItem of addedOrModified) {
        addAncestors(addItem, key);
        const itemData = findItemData(addItem.id, currentProv["element"]);
        if (itemData) {
          addDescendants(itemData, key);
        }
      }

      // Recursive function to remove descendants
      const removeDescendants = (item, key) => {
        if (item.children && item.children.length > 0) {
          for (const child of item.children) {
            selectedItems.value[key] = selectedItems.value[key].filter((el) => el.id !== child.id);
            removeDescendants(child, key); // Recursively remove child's descendants
          }
        }
      };

      for (const removedItem of removed) {
        const itemData = findItemData(removedItem.id, currentProv["element"]);
        if (itemData) {
          removeDescendants(itemData, key);
        }
      }






      }
    }


    //console.log("#######################  watch-end  #############################")
    // Update oldValue to reflect the new state
    oldValue = { ...newValue };
  },
  { deep: true }
)

const buildTree = (items) => {
  const idToNodeMap = {};
  const rootNodes = [];

  // Create a map of all items by their ID
  items.forEach(item => {
    idToNodeMap[item.id] = { ...item, children: [] };
  });

  // Link children to their respective parents
  items.forEach(item => {
    if (item.parent !== "false" && idToNodeMap[item.parent]) {
      idToNodeMap[item.parent].children.push(idToNodeMap[item.id]);
    } else {
      // If no parent, it is a root node
      rootNodes.push(idToNodeMap[item.id]);
    }
  });

  return rootNodes;
};


const getValues2link = computed(() => {
  const fullList = [];
  let count = 0;

  for (const key in selectedItems.value) {
    if (selectedItems.value[key].length > 0) {
      //console.log("getKEY",key)
      const [title, host] = key.split('#domain#');
      const provider = fCards.value.find(item => item.title === title);


      let obj = {
        id: key + count,
        title: title + " - " + host,
        provider: title,
        host: host,
        children: buildTree(selectedItems.value[key]),

      };
      fullList.push(obj);
      count++;
    }
  }

  return fullList;
});

const type_elements = ref({
    Dataset: "$mdiDatabase" ,
    Experiment: "$mdiFlask" ,
    Image: "$mdiImage" ,
    Project: "$mdiFolderMultipleImage",
    Spectra: "$mdiWaveform",
    other : "$mdiFile"
  })


</script>
