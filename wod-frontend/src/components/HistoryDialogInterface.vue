<template>
  <v-dialog width="600" height="1067" opacity="0">
    <template v-slot:activator="{props}">
      <v-btn v-bind="props" icon variant="text">
        <v-icon>mdi-history</v-icon>
      </v-btn>
    </template>
    <v-card style="
    background: linear-gradient(to bottom, rgba(234, 165, 250, 0.7), rgba(234, 211, 240, 0.7));
    scrollbar-width: thin;
  scrollbar-color: #e0e0e0 rgba(0, 0, 0, 0);
    ">
      <v-infinite-scroll @load="load">
        <template class="pa-2">
          <div v-for="(message, index) in items" :key="index" :class="['message-box', message.role]">
            <div class="message-content">
              {{ message.content }}
            </div>
          </div>
        </template>
      </v-infinite-scroll>
    </v-card>
  </v-dialog>
</template>
  
<script setup lang="ts">
  
    import { useAppStore } from '@/stores/app'
    import { ref } from 'vue'
  
    const prop = defineProps({
      companionId: {
        type: String,
        required: true
      }
    })
  
    const messageMap = useAppStore().messageMap
    const items = ref(messageMap.get(prop.companionId)?.slice(0, 20) || [])

    const load = () => {
      items.value.push(...(messageMap.get(prop.companionId) || []))
    }

    load()
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
  
    .message-box.assistant .message-content {
      background-color: #e0e0e0;
      /* 灰色，類似圖中對方訊息的顏色 */
      border-bottom-left-radius: 0;
    }
  
    .message-role {
      font-weight: bold;
    }
</style>