<template>
  <div style="position: absolute; z-index: 1;">
    <!--<v-container style="position: fixed; top: 20%; left: 60%;">
      <div v-if="store.messageMap.get(companionId)">
        <div v-for="(message, index) in store.messageMap.get(companionId)" :key="index"
          :class="['message-box', message.role]">
          <div class="message-content">
            {{ message.content }}
          </div>
        </div>
      </div>
    </v-container>-->

    <v-container style="position: fixed; top: 10%; left: 65%;">
      <div class="message-box">
        <div class="message-content">
          test
        </div>
      </div>
    </v-container>

    <v-form @submit.prevent="sendMessage">
      <v-footer app class="pa-0" style=" background: none">
        <v-container class="pa-2 pt-0">
          <v-text-field v-model="newMessage" append-icon="mdi-send" density="compact" flat hide-details label="說些什麼吧"
            single-line variant="solo" @click:append="sendMessage" style="width: 100%;" />
        </v-container>
      </v-footer>
    </v-form>
  </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/stores/app'
import { ref } from 'vue'

defineProps({
  companionId: {
    type: String,
    required: true
  }
})

const store = useAppStore()

// 新增訊息內容的變數
const newMessage = ref('')

// 發送訊息函數
const sendMessage = () => {
  if (newMessage.value.trim()) {
    newMessage.value = '' // 清空輸入框
  }
}
</script>

<style scoped>
  .message-box {
    display: flex;
    margin-bottom: 10px;
  }

  .message-box.bot {
    justify-content: flex-start;
  }

  .message-content {
    padding: 10px;
    border-radius: 15px;
    background-color: #f1f1f1;
    white-space: pre-wrap;
    color: black;
  }

  .message-box.bot .message-content {
    background-color: #e0e0e0;
    /* 灰色，類似圖中對方訊息的顏色 */
    border-bottom-left-radius: 0;
  }

  .message-role {
    font-weight: bold;
  }
</style>