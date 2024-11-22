<script setup>
import { init, setBackground } from '../components/index';
import { ref, onMounted } from 'vue';

// Background options
const backgrounds = [
  { name: 'Living Room', path: './src/assets/backgrounds/Living_room.jpg' },
  { name: 'Street 1', path: './src/assets/backgrounds/street.jpg' },
  { name: 'Street 2', path: './src/assets/backgrounds/street2.jpg' },
];

// State for the settings panel
const showSettings = ref(false);

// Change the background when an option is selected
const changeBackground = (background) => {
  setBackground(background.path);
};

// Initialize Live2D model
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
      overflow: hidden;
    "
  >
    <!-- Canvas for Live2D model -->
    <canvas
      id="canvas_view"
      style="
        display: block;
        margin: 0 auto;
        position: relative;
        z-index: 1;
      "
    ></canvas>

    <!-- Transparent settings button -->
    <button
      @click="showSettings = !showSettings"
      style="
        position: absolute;
        top: 10px;
        left: 10px;
        z-index: 2;
        width: 40px;
        height: 40px;
        border: none;
        background: transparent; /* Transparent background */
        color: white;
        font-size: 20px;
        cursor: pointer;
      "
      title="Settings"
    >
      ⚙
    </button>

    <!-- Settings panel with animations -->
    <div
      :class="{ 'settings-panel': true, visible: showSettings }"
      style="
        position: absolute;
        top: 60px;
        left: 10px;
        z-index: 3;
        width: 200px;
        background-color: rgba(0, 0, 0, 0.8);
        padding: 15px;
        border-radius: 8px;
        color: white;
      "
    >
      <h3 style="margin-top: 0; font-size: 16px;">Settings</h3>
      <p style="margin: 10px 0; font-size: 14px;">Change Background:</p>
      <div>
        <button
          v-for="background in backgrounds"
          :key="background.name"
          @click="changeBackground(background)"
          style="
            display: block;
            margin: 5px 0;
            padding: 10px 15px;
            font-size: 14px;
            border: none;
            border-radius: 4px;
            background-color: #3498db;
            color: white;
            cursor: pointer;
            text-align: left;
            width: 100%;
          "
        >
          {{ background.name }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Hover effect for the settings button */
button:hover {
  color: #3498db; /* Highlight icon color on hover */
  transform: scale(1.2); /* Slightly enlarge the button */
}

/* Animation for the settings panel */
.settings-panel {
  transition: opacity 0.3s ease, transform 0.3s ease; /* Smooth animation */
  transform: translateY(-10px); /* Slide up when hidden */
  opacity: 0; /* Fully transparent */
}

.settings-panel.visible {
  transform: translateY(0); /* Slide to position */
  opacity: 1; /* Fully visible */
}
</style>
