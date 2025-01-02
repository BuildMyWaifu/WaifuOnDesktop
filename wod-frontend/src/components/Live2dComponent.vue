<template>
  <div style="width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;" class="overflow-hidden">

    <canvas id="live2dCanvas" style="
    display: block;
    margin: 0 auto;
    position: relative;

    width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;
    "></canvas>
  </div>
</template>

<script setup lang="ts">
  import { onMounted } from 'vue';
  import { init } from '../utils/live2d'; // Import your Live2D setup logic

  const props = defineProps({
    fromUrl: {
      type: String,
      required: true
    }
  })

  onMounted(async () => {
    console.log('Live2DComponent: Mounted hook started...');
      try {
        await init("live2dCanvas", props.fromUrl);
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