<template>
  <v-layout style="width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;" class="overflow-hidden live-background">



    <canvas id="live2dCanvas" style="
    display: block;
    margin: 0 auto;
    position: relative;
    
    width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;
    "></canvas>
    <v-overlay v-model="loading" class="align-center justify-center" contained persistent>
      <v-progress-circular v-show="loading" indeterminate></v-progress-circular>
    </v-overlay>

  </v-layout>
</template>

<script setup lang="ts">
  import { onMounted, ref } from 'vue';
  import { init } from '../utils/live2d'; // Import your Live2D setup logic
  const loading = ref(false);
  const props = defineProps({
    fromUrl: {
      type: String,
      required: true
    }
  })

  onMounted(async () => {
    console.log('Live2DComponent: Mounted hook started...');
    try {
      loading.value = true;
      await init("live2dCanvas", props.fromUrl);
      loading.value = false;
      // alert('live2d init')
      console.log('Live2DComponent: Live2D model initialized successfully.');
    } catch (error) {
      alert(`Live2DComponent: Failed to initialize Live2D model: ${error}`);
    }
  });

  // onUpdated(async () => {
  //   try {
  //     await init("live2dCanvas");
  //     // alert('live2d init')
  //     console.log('Live2DComponent: Live2D model initialized successfully.');
  //   } catch (error) {
  //     alert('Live2DComponent: Failed to initialize Live2D model:', error);
  //   }
  //   return true;
  // })
</script>
<style>
  .live-background {
    background: rgb(255, 242, 114);
    background: linear-gradient(38deg, rgba(255, 242, 114, 1) 0%, rgba(207, 124, 205, 1) 100%);
  }
</style>