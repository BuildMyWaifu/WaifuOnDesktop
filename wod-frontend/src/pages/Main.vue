<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app location="left" :permanent="isPermanent">
      <v-list lines="three" select-strategy="single-independent">
        <template #prepend>
          <v-avatar /> <!-- avatar for waifu -->
        </template>
        <v-list-item
          v-for="companion in store.companionList"
          :key="companion._id"
          :value="companion._id"
          @click="updateCurrentWife(companion._id)"
        >
          <v-list-item-title>{{ companion._id }}</v-list-item-title>
          <v-list-item-subtitle>
            <div v-if="store.messageMap.get(companion._id)">
              {{ lastMessage(companion._id)?.content || 'No messages yet' }}
            </div>
          </v-list-item-subtitle>
        </v-list-item>
        <v-divider />
      </v-list>
      <template #append>
        <v-divider />
        <v-list-item v-if="store.user" lines="three">
          <v-list-item-title>
            {{ store.user?.profile.name }}
          </v-list-item-title>

          <template #append>
            <v-menu offset-y>
              <template #activator="{ props }">
                <v-btn v-bind="props" icon="mdi-cog" variant="text" />
              </template>
              <!-- 彈出選單內容 -->
              <v-list>
                <v-list-item @click="goToHome">
                  <v-list-item-title>回到主頁面</v-list-item-title>
                </v-list-item>
                <v-list-item @click="goToSettings">
                  <v-list-item-title>設定</v-list-item-title>
                </v-list-item>
                <v-list-item @click="logout">
                  <v-list-item-title>登出</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>
        </v-list-item>
      </template>
    </v-navigation-drawer>

    <v-app-bar>
      <template v-if="display.width.value < 500">
        <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      </template>
      <v-app-bar-title>
        {{ currentWife === null ? (currentWife || '老婆名稱') : currentWife }}
      </v-app-bar-title>
    </v-app-bar>

    <v-main>
      <v-container style="max-height: 80vh; overflow: auto">
        <!--chat interface-->
        <div v-if="store.messageMap.get('test 1')">
          <!--
          <div v-if="lastMessage('test 1')">
            Last message from waifu: {{ lastMessage('test 1')?.content || 'No messages yet' }}
          </div>
          -->
          <!-- 訊息列表 -->
          <v-list-item v-for="(message, index) in store.messageMap.get('test 1')" :key="index" :class="['message-box', message.role]">
            <v-list-item-title class="message-content">{{ message.content }}</v-list-item-title>
          </v-list-item>

        </div>
      </v-container>
      <!-- 新增訊息輸入欄 -->
      <v-container class="message-input-container">
        <v-row>
          <v-col cols="10">
            <v-text-field v-model="newMessage" dense label="輸入訊息..." outlined />
          </v-col>
          <v-col cols="1">
            <v-btn color="primary" icon="mdi-send" @click="sendMessage" />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
  import { useAppStore } from '@/stores/app'
  import { useDisplay } from 'vuetify'
  import { onMounted } from 'vue'

  const store = useAppStore()
  const router = useRouter()

  const display = useDisplay()

  // 控制 navigation drawer 的開關
  const drawer = ref(true) // 初始改為 undefined，即自動

  // currentWife 定義為一個 ref，這樣它可以是響應式的
  const currentWife = ref<string | null>(null)

  const windowISUpper500 = ref(display.width.value >= 500)
  const isPermanent = ref(display.width.value >= 500)

  // 新增訊息內容的變數
  const newMessage = ref('')

  // 發送訊息函數
  const sendMessage = () => {
    if (newMessage.value.trim()) {
      newMessage.value = '' // 清空輸入框
    }
  }

  const lastMessage = (Id: string) => {
    const messages = store.messageMap.get(Id)
    return messages ? messages[messages.length - 1] : null
  }

  // updateCurrentWife 函數來更新 currentWife
  const updateCurrentWife = (Id: string) => {
    currentWife.value = Id
  }

  const goToHome = () => {
    router.push('/')
  }

  const goToSettings = () => {
    console.log('Setting')
  }

  const logout = () => {
    store.logout()
    router.push('/')
  }

  // 監聽 window 的 resize 事件，並在 window 尺寸改變時調整 drawer 的狀態
  onMounted(() => {
    window.addEventListener('resize', handleResize)
    handleResize()
  })
  const handleResize = () => {
    if (windowISUpper500.value && display.width.value < 500) {
      drawer.value = false
      windowISUpper500.value = false
      isPermanent.value = false
    } else if (!windowISUpper500.value && display.width.value >= 500) {
      drawer.value = true
      windowISUpper500.value = true
      isPermanent.value = true
    }
  }
</script>

<style scoped>
.message-box {
  display: flex;
  margin-bottom: 10px;
  max-width: 60%;
}

.message-box.user {
  justify-content: flex-end;
}

.message-box.wife {
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
  background-color: #b2dfdb; /* 淺綠色，類似圖中訊息的顏色 */
  border-bottom-right-radius: 0;
}

.message-box.wife .message-content {
  background-color: #e0e0e0; /* 灰色，類似圖中對方訊息的顏色 */
  border-bottom-left-radius: 0;
}

.message-role {
  font-weight: bold;
}

.message-input-container {
  background-color: #fafafa;
  padding: 10px;
  border-top: 1px solid #ccc;
  overflow: auto;
}
</style>
