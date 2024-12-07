<template>
  <div
    class="speech-bubble"
    v-if="visible"
    :style="bubblePosition"
  >
    <p>{{ message }}</p>
    <div class="speech-bubble-arrow"></div>
  </div>
</template>

<script setup>
import { computed, toRefs } from 'vue';

const props = defineProps({
  message: {
    type: String,
  },
  visible: {
    type: Boolean,
    default: false
  },
  x: {
    type: Number,
    default: 0
  },
  y: {
    type: Number,
    default: 0
  }
});

const bubblePosition = computed(() => {
  return {
    position: 'absolute',
    top: `${props.y}px`,
    left: `${props.x}px`,
  };
});
</script>

<style scoped>
.speech-bubble {
  min-height: 100px;
  min-width: 300px;
  max-width: 1000px;
  /* Use a semi-transparent background for the bubble */
  background: rgba(255, 255, 255, 0.8);
  color: #333;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);
  position: relative;
  font-size: 16px;
  line-height: 1.6;
}


</style>
