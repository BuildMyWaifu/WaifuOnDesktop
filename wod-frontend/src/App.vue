<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
  import { useAppStore } from './stores/app'
  import { onMounted } from 'vue';
  import { setBroadcastCallback, fetchSync } from './utils/electronAPI';

  const store = useAppStore()
  onMounted(() => {
  console.log('App.vue: Mounted hook executed.');
  try {
    fetchSync(); 
    setBroadcastCallback((sync) => {
      store.setSync(sync);
    });
  } catch (error) {
    console.error('App.vue: Error in mounted hook:', error);
  }
});


</script>
