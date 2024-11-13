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

  const store = useAppStore()
  onMounted(store.generateMockMessages)
</script>
