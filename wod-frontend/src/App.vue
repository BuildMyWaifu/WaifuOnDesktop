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
    store.generateMockMessages()
    fetchSync()
    setBroadcastCallback((sync) => {
      store.setSync(sync)
    })
  }
  )

</script>
