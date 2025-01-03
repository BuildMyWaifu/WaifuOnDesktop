<template>
  <v-dialog width="600" height="1067" opacity="0">
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props" icon variant="text">
        <v-icon>mdi-history</v-icon>
      </v-btn>
    </template>
    <v-card style="
    background: linear-gradient(to bottom, rgba(234, 165, 250, 0.7), rgba(234, 211, 240, 0.7));
    scrollbar-width: thin;
  scrollbar-color: #e0e0e0 rgba(0, 0, 0, 0);
    ">
      <v-card-text v-if="messageList.length == 0" class="text-center h-100 w-100 flex-grow-1">
          目前沒有任何訊息
      </v-card-text>
      <v-card-text class="pr-0 h-100 w-100">
        <v-infinite-scroll @load="load" side="both" empty-text="" class="pr-4 h-100 w-100">
          <template v-for="message in messageList" :key="message._id">
            <div :class="['message-box', message.role]">
              <div class="message-content">
                {{ message.content }}
              </div>
            </div>
          </template>
        </v-infinite-scroll>

      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">

  import { useAppStore } from '@/stores/app'
  import { fetchApi, handleErrorAlert } from '@/utils/api'
  import { Message } from '@/utils/model'
  import { computed } from 'vue'

  const prop = defineProps({
    companionId: {
      type: String,
      required: true
    }
  })
  const store = useAppStore()

  const messageList = computed(() => {
    return store.messageMap.get(prop.companionId) || []
  })

  async function load({
    side, done,
  }: {
    side: "start" | "end" | "both";
    done: (status: "loading" | "error" | "empty" | "ok") => void;
    }) {
    if (side == "start") {
     
      let before = Date.now();
      
      if (messageList.value.length != 0) {
        
        const timestamp = messageList.value[0].createdAt;
        if (!timestamp) {
          alert(
            `存在一個沒有建立時間的訊息 ${messageList.value[0]._id} 請將此訊息告知開發人員`
          );
          return;
        }
        before = timestamp;
      }
      
      const res = handleErrorAlert(await fetchApi(`/message/${prop.companionId}?before=${before}`)) as Array<Message>;
        if (res == undefined) {
          return done("error");
        }
        if (res.length == 0) {
          return done("empty");
        }
        store.addMessageListToFront(prop.companionId, res);
        done("ok");
    }
    if (side == "end") {
      let after = 0;

      if (messageList.value.length != 0) {

        const timestamp = messageList.value[messageList.value.length-1].createdAt;
        if (!timestamp) {
          alert(
            `存在一個沒有建立時間的訊息 ${messageList.value[0]._id} 請將此訊息告知開發人員`
          );
          return;
        }
        after = timestamp;
      }

      const res = handleErrorAlert(await fetchApi(`/message/${prop.companionId}?after=${after}`)) as Array<Message>;
      if (res == undefined) {
        return done("error");
      }
      if (res.length == 0) {
        return done("empty");
      }
      store.addMessageListToBack(prop.companionId, res);
      done("ok");
    }
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

  .message-box.assistant .message-content {
    background-color: #e0e0e0;
    /* 灰色，類似圖中對方訊息的顏色 */
    border-bottom-left-radius: 0;
  }

  .message-role {
    font-weight: bold;
  }
</style>