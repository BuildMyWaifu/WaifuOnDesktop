<template>
  <div style="
  height: 100vh;
      width: 100vw;
      overflow: hidden;
    " v-if="companion">
    <div style="position: fixed; top: 0; left: 0;z-index: 100" class="w-100 h-100 d-flex justify-center">
      <v-container style="margin-top: 8vh; max-width: 800px; max-height: 80%;"
        class="d-flex flex-column align-start fade-container">
        <SpeechBubble :message="message.content" class="mt-4" style="max-width: 300px;"
          v-for="message in recvMessageList" :key="message._id" />
      </v-container>
    </div>

    <Live2DComponent :fromUrl="companion.live2dModelSettingPath" style="z-index: 1;" id="live2dComponent" />

    <div>
      <div class="floating-chat">
        <textarea :disabled="messageLoading" v-model="message" placeholder="請輸入想要傳送的訊息..."
          @keypress.enter.exact.prevent="handleEnter" class="chat-input"></textarea>
        <v-btn :loading="messageLoading" @click="sendMessage" variant="text" icon flat
          color="primary"><v-icon>mdi-send</v-icon></v-btn>
      </div>
    </div>

    <div style="
     position: fixed;
     top: 10px;
     left: 10px;
     z-index: 200;
   ">
      <v-btn :to="`/app/${companionId}`" prepend-icon="mdi-menu" variant="text">返回選單</v-btn>
      <HistoryDialogInterface v-if="companionId" :companionId="companionId" />
      <v-menu :close-on-content-click="false">
        <template v-slot:activator="{props}">
          <v-btn v-bind="props" icon variant="text"><v-icon>mdi-wallpaper</v-icon></v-btn>
        </template>
        <v-list>
          <v-list-item @click="setBackground()">清除背景</v-list-item>
          <v-list-item @click="setBackground('/backgrounds/Living_room.jpg')">和風室內</v-list-item>
          <v-list-item @click="setBackground('/backgrounds/street.jpg')">房屋前</v-list-item>
          <v-list-item @click="setBackground('/backgrounds/street2.jpg')">馬路上</v-list-item>
          <v-divider></v-divider>
          <v-dialog width="500">
            <template v-slot:activator="{props}">
              <v-list-item v-bind="props">自定義</v-list-item>
            </template>
            <!-- <v-list-item @click="setBackground('/backgrounds/forest.jpg')">自定義</v-list-item> -->
             <v-card>
              <v-card-text>
                <v-file-input :disabled="setupLoading" :loading="setupLoading" type="file" accept="image/*" label="上傳自定義背景" @change="handleSetBackground" hide-details></v-file-input>
              </v-card-text>
             </v-card>
          </v-dialog>
        </v-list>
      </v-menu>
      <!-- History Dialog Button -->

    </div>
  </div>
  <v-dialog :model-value="setupLoading" persistent width="350">
    <v-card class="text-center" title="正在初始化角色">
      <v-card-subtitle class="text-wrap">正在使用LLM生成更詳細的對話設定<br>這個過程需要十秒左右...</v-card-subtitle>
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
  import { fetchApi, handleErrorAlert, postApi } from '@/utils/api';

  const recvMessageList = ref<Message[]>([])
  const setupLoading = ref(false);

  const route = useRoute();
  const router = useRouter();

  const store = useAppStore()

  const message = ref('');

  const companion = computed(() => {
    if (companionId.value == undefined) return undefined
    return store.getCompanion(companionId.value)
  })
  const messageLoading = ref(false)

  async function sendMessage() {


    if (setupLoading.value) return
    if (messageLoading.value) return
    messageLoading.value = true

    const recvMessge = handleErrorAlert(await postApi(`/message`, {
      companionId: companionId.value,
      content: message.value
    })) as Message
    // insert at 0
    if (recvMessge.pose) {
      if (recvMessge.pose.expression) {
        store.pushExpression(recvMessge.pose.expression)
      }
      if (recvMessge.pose.motion) {
        store.pushMotion(recvMessge.pose.motion)
      }
    }
    recvMessageList.value = [recvMessge, ...recvMessageList.value]
    message.value = ''; // Clear the input after sending
    messageLoading.value = false
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
  // Existing setBackground function remains the same
  function setBackground( imagePath?: string) {
    const container = document.getElementById('live2dComponent');
    if (container) {
      if (!imagePath) {
        container.style.backgroundImage = '';
       
        return;
      }
      container.style.backgroundImage = `url('${imagePath}')`;
      container.style.backgroundRepeat = 'no-repeat';
      container.style.backgroundPosition = 'center';
      container.style.backgroundSize = 'cover';
      // container.style.zIndex = '1';
      console.log(`live2d.js: Background switched to ${imagePath}`);
    }
  }

  const companionId = ref<string>()
  // const companion = computed(() => {
  //   return store.getCompanion(companionId.value)
  // })
  onMounted(async () => {
    if ('companionId' in route.params && route.params.companionId) {
      companionId.value = route.params.companionId as string
    }
    else {
      alert("沒有指定聊天的伴侶，這不應該發生")
      router.push("/app")
      return
    }
    if (!companion.value?.trait) {
      setupLoading.value = true
      await fetchApi(`/companion/${companionId.value}/setup`)
      await store.loadCompanionList()
      setupLoading.value = false
    }
  })

  async function handleSetBackground(event: Event) {
    let files = (event.target as HTMLInputElement).files;
    if (!files) return;
    let file = undefined as File | undefined;
    if (!(files instanceof File)) {
      file = files[0];
    }
    else {
      file = files;
    }
    if (file.type.indexOf("image") == -1) {
      alert("請上傳有效的圖片檔案");
      return;
    }
    const reader = new FileReader();
    reader.onload = function (e) {
      setBackground(e.target?.result as string);
    }
    reader.readAsDataURL(file);
  }

</script>
<style scoped>
  .fade-container {
    -webkit-mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 30%, rgba(0, 0, 0, 0) 60%);
    mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 30%, rgba(0, 0, 0, 0) 60%);
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

  .fade-out-animation {
    animation: fadeOut 20s ease-out forwards;
  }

  @keyframes fadeOut {
    from {
      opacity: 1;
    }

    to {
      opacity: 0;
    }
  }
</style>
