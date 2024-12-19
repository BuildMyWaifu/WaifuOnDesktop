<template>
  <div
    class="speech-bubble"
  >
    <p>{{ message }}</p>
    <div class="speech-bubble-arrow"></div>
  </div>
</template>

<script setup>

defineProps({
  message: {
    type: String,
  },
})

</script>

<style scoped>
.speech-bubble {
  
  
  max-width: 1000px;
  /* Use a semi-transparent background for the bubble */
  background: rgba(255, 255, 255, 0.8);
  color: #333;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);

  font-size: 16px;
  line-height: 1.6;

  display: inline-block;
}


</style>
