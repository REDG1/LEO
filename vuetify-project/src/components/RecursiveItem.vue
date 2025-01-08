<template>
  <div>
    <v-container>
      <v-row no-gutters>
        <v-col v-for="(value, key) in data" :key="key" class="pa-1 ma-1">
          <strong>[[ key ]]:</strong>
          <div v-if="isObject(value)" class="">
            <RecursiveItem :data="value" />
          </div>
          <div v-else-if="Array.isArray(value)">
            <ul class="">
              <li v-for="(item, index) in value" :key="index"> [[ item ]]</li>
            </ul>
          </div>
          <div v-else-if="isHtmlKey(key)" v-html="value"></div>
          <div v-else>[[ value ]]</div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: 'RecursiveItem',
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  methods: {
    isObject(val) {
      return val !== null && typeof val === 'object' && !Array.isArray(val);
    },
    isHtmlKey(key) {
      return key.toLowerCase().includes('html');
    }
  }
};
</script>

<style scoped>
/* Add any custom styles here */
</style>
