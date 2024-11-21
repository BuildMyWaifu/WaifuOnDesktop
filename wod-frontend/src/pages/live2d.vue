<script setup>
import { init } from '../components/index';
import { onMounted } from 'vue';

onMounted(() => {
  console.log('live2d.vue: Mounted hook started...');
  try {
    init();
    console.log('live2d.vue: init() called successfully...');
  } catch (error) {
    console.error('live2d.vue: Error occurred in mounted hook:', error);
  }
});
</script>



<template>
  <div
    style="
      width: 100%;
      height: 100%;
      position: relative;
      overflow: auto; /* Allow scrolling */
      background: black; /* Optional background for better visibility */
    "
  >
    <canvas
      id="canvas_view"
      style="
        display: block;
        margin: 0 auto; /* Center horizontally */
        position: relative;
      "
    ></canvas>
  </div>
</template>

<style scoped>
#canvas_view {
  display: block;
}
</style>
