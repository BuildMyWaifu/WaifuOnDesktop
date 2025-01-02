<template>
  <div style="
      width: 100%;
      height: 100%;
      position: relative;
      overflow: hidden;
    " v-if="companion">
    <div style="position: fixed; top: 0; left: 0;z-index: 100" class="w-100 h-100 d-flex justify-center">
      <v-container style="margin-top: 8vh; max-width: 800px; max-height: 80%;"
        class="d-flex flex-column align-start fade-container">
        <SpeechBubble :message="message.content" class="mt-4" v-for="message in companionMsgList" :key="message._id" />
      </v-container>
    </div>

    <Live2DComponent :fromUrl="companion.live2dModelSettingPath" />

    <v-overlay v-model="showHistoryDialog" style="z-index: 201;">
      <HistoryDialogInterface v-if="companionId" :companionId="companionId" @close="showHistoryDialog = false" />
    </v-overlay>

    <div>
      <div class="floating-chat">
        <button @click="showHistoryDialog = true">
          <v-icon>mdi-text-long</v-icon>
        </button>
        <textarea v-model="message" placeholder="請輸入想要傳送的訊息..." @keydown.enter.prevent="handleEnter"
          class="chat-input"></textarea>
        <v-btn @click="sendMessage" variant="text" icon flat color="primary"><v-icon>mdi-send</v-icon></v-btn>
      </div>
    </div>

    <div style="
     position: fixed;
     top: 10px;
     left: 10px;
     z-index: 200;
   ">
      <v-btn :to="`/app/${companionId}`" prepend-icon="mdi-menu" variant="text">返回選單</v-btn>
      <!-- History Dialog Button -->

    </div>

    <!-- Close History Dialog Button -->
    <button v-if="showHistoryDialog" @click="showHistoryDialog = false" style="
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 202;
    background-color: rgb(237, 172, 231);
    color: rgb(255, 255, 255);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    align-items: center;
    justify-content: center;
    box-shadow: rgba(71, 17, 77, 0.82);
    ">
      <v-icon>mdi-redo</v-icon>
    </button>
  </div>
  <v-dialog :model-value="loading" persistent width="350">
    <v-card class="text-center" title="正在初始化角色" subtitle="正在使用LLM生成更詳細的對話設定，這個過程需要十秒左右...">
      <v-card-text>
        <v-progress-linear indeterminate color="primary"></v-progress-linear>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
  import Live2DComponent from '../components/Live2dComponent.vue'; // Import your Live2D component
  import HistoryDialogInterface from '@/components/HistoryDialogInterface.vue';
  import SpeechBubble from '../components/SpeechBubble.vue';

  import { ref, onMounted, computed, nextTick } from 'vue';
  import { useRouter, useRoute } from 'vue-router'

  import { useAppStore } from '@/stores/app';
  import { Message } from '@/utils/model';
  import { fetchApi } from '@/utils/api';

  const loading = ref(false);

  const route = useRoute();
  const router = useRouter();

  const store = useAppStore()

  const message = ref('');

  const showHistoryDialog = ref(false);

  const companion = computed(() => {
    if (companionId.value == undefined) return undefined
    return store.getCompanion(companionId.value)
  })

  async function sendMessage() {
    if (loading.value) return
    alert(`Message sent ${message.value.trim()}`);
    message.value = ''; // Clear the input after sending
  }
  async function handleEnter(event: KeyboardEvent) {
    if (event) { 
      if (event.key === 'Enter') {
        if (!event.shiftKey) {
          await sendMessage()
          event.preventDefault();
        }
        else {
          const textarea = event.target;
          if (!(textarea instanceof HTMLTextAreaElement)) return;
          const start = textarea.selectionStart;
          const end = textarea.selectionEnd;
        
        // 在光標位置插入換行
        message.value = message.value.substring(0, start) + "\n" + message.value.substring(end);
        nextTick(() => {
          textarea.selectionStart = textarea.selectionEnd = start + 1;
        });
      }
    }
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

  const companionId = ref<string>()
  // const companion = computed(() => {
  //   return store.getCompanion(companionId.value)
  // })
  onMounted(async () => {
    if ('companionId' in route.params && route.params.companionId) {
      companionId.value = route.params.companionId as string
    }
    else {
      alert("沒有指定聊天的伴侶")
      router.push("/app")
    }
    if (!companion.value?.trait) { 
      loading.value = true
      await fetchApi(`/companion/${companionId.value}/setup`)
      loading.value = false
      // alert("伴侶資料尚未載入")
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
