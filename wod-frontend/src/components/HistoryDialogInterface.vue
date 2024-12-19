<template>
  <v-infinite-scroll :onLoad="load" :items="items" style="
  position: fixed;
  top:0px;
  left:0px;
  height: 100%;
  width: 100%;
  z-index: 201;
  background-color: rgba(234, 165, 250, 0.7);
  overflow-y: scroll;
  scrollbar-width: thin;
  scrollbar-color: #e0e0e0 rgba(0, 0, 0, 0);
  ">
    <div class="pa-2">
      <!--test-->
      <div v-for="(item, index) in items" :key="item" class="message-box" :class="index % 2 === 1 ? 'user' : 'bot'">
        <div class="message-content">
          {{ index % 2 === 1 ? 'user test message' : 'bot test message' }}
        </div>
      </div>
    </div>
  </v-infinite-scroll>
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
    const items = ref(Array.from({ length: 20 }, (k, v) => v + 1))

    async function api () {
      return new Promise(resolve => {
        setTimeout(() => {
          resolve(Array.from({ length:10 }, (k, v) => v + (items.value.at(-1) ?? 0) + 1))
        }, 1000)
      })
    }

    async function load ({ done }) {
      // Perform API call
      const res = await api()

      items.value.push(...res)

      done('ok')
    }
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