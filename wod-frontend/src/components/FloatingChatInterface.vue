<template>
  <div class="floating-chat">
    <textarea
      v-model="message"
      placeholder="What do you wnat to say, my dear..."
      @keydown.enter="sendMessage"
      class="chat-input"
    ></textarea>
    <button @click="sendMessage" class="send-button">Send</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const message = ref('');

const sendMessage = () => {
  if (message.value.trim() !== '') {
    console.log('Message sent:', message.value);
    message.value = ''; // Clear the input after sending
  }
};
</script>

<style scoped>
.floating-chat {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 100;
  display: flex;
  align-items: center; /* Keeps items aligned vertically center */
  background-color: rgba(0, 0, 0, 0.7);
  border-radius: 120px;
  padding: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);

  /* Add this to make the chat box longer horizontally */
  min-width: 400px; /* Increase this value as needed */
}

.chat-input {
  flex: 1;
  background-color: transparent;
  border: none;
  color: white;
  font-size: 14px;

  /* Increase padding to give more vertical space, making the placeholder appear centered */
  padding: 12px 8px;

  /* Set a line-height to help with vertical centering of text */
  line-height: 1.5;

  outline: none;
  resize: none;
}

.chat-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
  /* The vertical centering of placeholder is controlled by the padding and line-height above */
}

.send-button {
  background-color: #3498db;
  border: none;
  color: white;
  font-size: 14px;
  padding: 8px 12px;
  border-radius: 50px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.send-button:hover {
  background-color: #2980b9;
}
</style>
