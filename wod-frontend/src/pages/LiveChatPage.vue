<template>

  <div style="
      width: 100%;
      height: 100%;
      position: relative;
      overflow: hidden;
    ">

    <div style="position: fixed; top: 0; left: 0;z-index: 100" class="w-100 h-100 d-flex justify-center">
      <v-container style="margin-top: 8vh; max-width: 800px; max-height: 80%;"
        class="d-flex flex-column align-start fade-container">
        <SpeechBubble :message="message.content" class="mt-4" v-for="message in companionMsgList" :key="message._id" />
      </v-container>
    </div>

    <Live2DComponent />
    <div>
      <div class="floating-chat">
        
        <textarea v-model="message" placeholder="What do you wnat to say, my dear..." @keydown.enter="sendMessage"
        class="chat-input"></textarea>
        <button @click="sendMessage" class="send-button">Send</button>
      </div>
    </div>

    <div style="
     position: fixed;
     top: 10px;
     left: 10px;
     z-index: 200;
   ">
      <v-btn to="/">返回首頁</v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, computed } from 'vue';
  import Live2DComponent from '../components/Live2dComponent.vue'; // Import your Live2D component

  import SpeechBubble from '../components/SpeechBubble.vue';
  import { useAppStore } from '@/stores/app';
  import { Message } from '@/utils/model';


  const store = useAppStore()

  const message = ref('');

  const sendMessage = () => {
    if (message.value.trim() !== '') {
      console.log('Message sent:', message.value);
      message.value = ''; // Clear the input after sending
    }
  };

  function getMessageList(): Message[] {
    if (companionId.value == undefined) return []
    const result = store.messageMap.get(companionId.value)
    if (!result) return []
    else return result
  }



  const companionMsgList = computed<Message[]>(() => {
    return getMessageList().filter((msg) => {
      return msg.role == 'bot'
    })
  })

  const companionId = ref<string>()  // 正常來說，會需要透過 props 來傳入這個參數，不過目前測試時先這樣用就夠了

  onMounted(() => {
    store.generateMockCompanionList()
    store.generateMockMessages()
    if (companionId.value == undefined) {
      if (!store.companionList || store.companionList.length == 0) return
      companionId.value = store.companionList[0]._id
    }
  })


</script>
<style scoped>
  .fade-container {
    -webkit-mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 70%, rgba(0, 0, 0, 0) 100%);
    mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 70%, rgba(0, 0, 0, 0) 100%);
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
    -webkit-mask-size: 100% 100%;
    mask-size: 100% 100%;
  }

  .floating-chat {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 100;
    display: flex;
    align-items: center;
    /* Keeps items aligned vertically center */
    background-color: rgba(0, 0, 0, 0.7);
    border-radius: 120px;
    padding: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);

    /* Add this to make the chat box longer horizontally */
    min-width: 400px;
    /* Increase this value as needed */
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
