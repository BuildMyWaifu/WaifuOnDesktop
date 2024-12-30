<template>
  <div style="width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;" class="overflow-hidden">

    <canvas v-if="elementId" :id="elementId" style="
    display: block;
    margin: 0 auto;
    position: relative;
    z-index: 1;
    width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;
    "></canvas>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, nextTick } from 'vue';
  import { init } from '../utils/live2d'; // Import your Live2D setup logic

  const elementId = ref<string>(crypto.randomUUID() + "_live2d");
  onMounted(async () => {
    console.log('Live2DComponent: Mounted hook started...');

    nextTick(async () => {

      try {
        await init(elementId.value);
        console.log('Live2DComponent: Live2D model initialized successfully.');
      } catch (error) {
        console.error('Live2DComponent: Failed to initialize Live2D model:', error);
      }
    })
  });
</script>