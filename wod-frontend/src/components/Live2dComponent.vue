<template>
  <canvas
    id="canvas_view"
    style="
      display: block;
      margin: 0 auto;
      position: relative;
      z-index: 1;
      width: 100%;
      height: 100%;
    "
  ></canvas>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { init } from '../utils/live2d'; // Import your Live2D setup logic

// State for error handling
const isModelLoaded = ref(false);

onMounted(async () => {
  console.log('Live2DComponent: Mounted hook started...');
  try {
    await init();
    isModelLoaded.value = true;
    console.log('Live2DComponent: Live2D model initialized successfully.');
  } catch (error) {
    isModelLoaded.value = false;
    console.error('Live2DComponent: Failed to initialize Live2D model:', error);
  }
});
</script>

<style scoped>
/* Add any specific styling for the canvas if needed */
canvas {
  width: 100%;
  height: 100%;
}
</style>
