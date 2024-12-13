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
    <FloatingChatInterface />

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

  import FloatingChatInterface from '../components/FloatingChatInterface.vue';
  import SpeechBubble from '../components/SpeechBubble.vue';
  import { useAppStore } from '@/stores/app';
  import { Message } from '@/utils/model';

  const store = useAppStore()

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
</style>
