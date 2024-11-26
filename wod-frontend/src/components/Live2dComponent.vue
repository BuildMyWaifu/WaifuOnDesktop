
<template>
  <div
    style="
      width: 100%;
      height: 100%;
      position: relative;
      overflow: hidden;
    "
  >
    <!-- Video Background -->
    <video
      v-if="activeVideo"
      :src="activeVideo"
      autoplay
      muted
      loop
      playsinline
      style="
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
        z-index: 0;
      "
    ></video>

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
    <-- <button 
      @click="showSettings = !showSettings"
      style="
        position: absolute;
        top: 10px;
        left: 10px;
        z-index: 2;
        width: 40px;
        height: 40px;
        border: none;
        background: transparent;
        color: white;
        font-size: 20px;
        cursor: pointer;
      "
      title="Settings"
    >
      ⚙
    </button> -->

    <!-- Settings panel -->
    <div
      v-if="showSettings"
      :class="{ 'settings-panel': true, visible: showSettings }"
      style="
        position: absolute;
        top: 60px;
        left: 10px;
        z-index: 3;
        width: 250px;
        background-color: rgba(0, 0, 0, 0.85);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        color: white;
      "
    >
      <h3 style="margin-top: 0; font-size: 18px; text-align: center;">Settings</h3>
      <p style="margin: 10px 0; font-size: 16px; text-align: center;">Change Background:</p>
      <div style="display: flex; flex-direction: column; align-items: center; gap: 10px;">
        <button
          v-for="background in backgrounds"
          :key="background.name"
          @click="changeBackground(background)"
          style="
            width: 100%;
            padding: 12px 20px;
            font-size: 14px;
            border: none;
            border-radius: 8px;
            background: linear-gradient(120deg, #3498db, #2ecc71);
            color: white;
            cursor: pointer;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
          "
          @mouseover="this.style.transform = 'scale(1.05)'"
          @mouseleave="this.style.transform = 'scale(1)'"
        >
          {{ background.name }}
        </button>
      </div>

      <!-- Custom upload button -->
      <div style="margin-top: 20px; text-align: center;">
        <label style="font-size: 14px; display: block; margin-bottom: 10px;">Custom Background:</label>
        <div style="position: relative;">
          <input
            type="file"
            accept="image/jpeg, image/png, video/mp4"
            @change="handleFileUpload"
            style="
              position: absolute;
              opacity: 0;
              width: 100%;
              height: 100%;
              cursor: pointer;
            "
          />
          <button
            style="
              display: block;
              width: 100%;
              padding: 12px 20px;
              font-size: 14px;
              border: none;
              border-radius: 8px;
              background: linear-gradient(120deg, #9b59b6, #8e44ad);
              color: white;
              cursor: pointer;
              text-align: center;
              box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
              transition: transform 0.2s ease, box-shadow 0.2s ease;
            "
            @mouseover="this.style.transform = 'scale(1.05)'"
            @mouseleave="this.style.transform = 'scale(1)'"
          >
            Upload
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { init, setBackground } from './index';
import { ref, onMounted } from 'vue';

// Background options
const backgrounds = [
  { name: 'Living Room', type: 'image', path: './src/assets/backgrounds/Living_room.jpg' },
  { name: 'Street 1', type: 'image', path: './src/assets/backgrounds/street.jpg' },
  { name: 'Street 2', type: 'image', path: './src/assets/backgrounds/street2.jpg' },
  { name: 'Mountain (Video)', type: 'video', path: './src/assets/backgrounds/Mountain_anime.mp4' },
];

// State for the settings panel
const showSettings = ref(false);
const activeVideo = ref(null); // Keeps track of the currently active video background

// Change the background
const changeBackground = (background) => {
  if (background.type === 'video') {
    activeVideo.value = background.path; // Set active video path
    setBackground(null); // Disable image background
  } else {
    activeVideo.value = null; // Clear active video
    setBackground(background.path); // Set image background
  }
};

// Handle user-uploaded background
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const fileType = file.type;
  if (fileType.startsWith('image/')) {
    const url = URL.createObjectURL(file); // Image file: create blob URL
    activeVideo.value = null; // Clear active video
    setBackground(url);
    console.log('Uploaded image set as background:', url);
  } else if (fileType === 'video/mp4') {
    const url = URL.createObjectURL(file); // Video file: create blob URL
    activeVideo.value = url;
    setBackground(null); // Disable image background
    console.log('Uploaded video set as background:', url);
  } else {
    alert('Unsupported file format. Please upload a .jpg, .png, or .mp4 file.');
  }

  event.target.value = ''; // Clear the input value for re-uploading the same file
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

<style scoped>
/* Hover effect for the settings button */
button:hover {
  color: #f1c40f;
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
