<template>
  <canvas v-if="loaded" :id="canvasId" style="
      display: block;
      margin: 0 auto;
      position: relative;
      z-index: 1;
      width: 100%;
      height: 100%;
    "></canvas>
</template>

<script setup lang="ts">
  import { ref, onMounted, nextTick } from 'vue';
  import { init } from '../utils/live2d'; // Import your Live2D setup logic


  const loaded = ref(false)

  const canvasId = ref<string>()

  // State for error handling
  const isModelLoaded = ref(false);

  onMounted(async () => {
    console.log('Live2DComponent: Mounted hook started...');
    canvasId.value = `live2d_canvas_${Math.random()}_${Date.now()}`

    loaded.value = true
    nextTick(async () => {
      try {
        const modelPath = `../../src/assets/miku_model/runtime/miku_sample_t04.model3.json`;
        await init(canvasId.value, modelPath);
        isModelLoaded.value = true;
        console.log('Live2DComponent: Live2D model initialized successfully.');
      } catch (error) {
        isModelLoaded.value = false;
        console.error('Live2DComponent: Failed to initialize Live2D model:', error);
      }  
    })
    

  });
</script>
<style scoped>

  /* Add any specific styling for the canvas if needed */
  canvas {
    width: 100%;
    height: 100%;
  }
</style>
