<template>
    <!--<v-main style="height: 100vh">
        <v-container class="pa-2" style="height: 100%;">
            <div v-if="store.messageMap.get(companionId)">
                <div v-for="(message, index) in store.messageMap.get(companionId)" :key="index"
                :class="['message-box', message.role]">
                    <div class="message-content">
                        {{ message.content }}
                    </div>
                </div>
            </div>
        </v-container>
  </v-main>-->
  <v-main>
    <v-container class="pa-2" style="height: 100%; overflow-y: scroll">
      <!--chat interface-->
      <div>
        <div class="message-box">
          <div class="message-content">
            test
          </div>
        </div>
      </div>
    </v-container>
  </v-main>
</template>
  
<script setup lang="ts">
  
    import { useAppStore } from '@/stores/app'
    import {  ref } from 'vue'
  
    defineProps({
      companionId: {
        type: String,
        required: true
      }
    })
  
    const store = useAppStore()
</script>
  
<style scoped>
    .message-box {
      display: flex;
      margin-bottom: 10px;
    }
  
    .message-box.user {
      justify-content: flex-end;
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
  
    .message-box.user .message-content {
      background-color: #b2dfdb;
      /* 淺綠色，類似圖中訊息的顏色 */
      border-bottom-right-radius: 0;
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