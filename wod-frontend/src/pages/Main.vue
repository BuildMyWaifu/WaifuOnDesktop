<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <v-navigation-drawer v-model="leftDrawer" app location="left" :permanent="isPermanentLeft">
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
      <div class="text-center">
        <v-btn @click="createNewWife">
          <template v-slot:prepend>
            <v-icon icon="mdi-plus"></v-icon>
          </template>
          新增老婆
        </v-btn>
      </div>
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
                <v-list-item to="/">
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
    
    <!-- 右側 -->
    <v-navigation-drawer v-model="rightDrawer" location="right" :permanent="isPermanentRight">
      <v-container class="d-flex flex-column align-center pt-10" style="height: 100%;">

        <v-sheet class="mb-4" width="60%" color="grey" style="aspect-ratio: 1; border: 4px solid gray; border-radius: 10%;">
          <v-img src="https://upload.wikimedia.org/wikipedia/zh/thumb/f/fc/%E5%8E%9F%E7%A5%9E_%E5%9C%8B%E9%9A%9B%E7%89%88.jpeg/220px-%E5%8E%9F%E7%A5%9E_%E5%9C%8B%E9%9A%9B%E7%89%88.jpeg" 
          alt="image" max-width="100%" max-height="100%" contain style="border-radius: 10%;"></v-img>
        </v-sheet>

        <v-row justify="center">
          <v-col class="text-center">
            <v-card-title class="text-h5">
              原神
            </v-card-title>
            <v-card-text class="text-h7">
              你說的對，但是《原神》是由米哈游自主研發的一款全新開放世界冒險遊戲。遊戲發生在一個被稱作「提瓦特」的幻想世界，在這裡，被神選中的人將被授予「神之眼」，導引元素之力。
            </v-card-text>
            
          </v-col>
        </v-row>
      </v-container>
    </v-navigation-drawer>

    <v-app-bar elevation="0">
      <template v-if="display.width.value < 750">
        <v-app-bar-nav-icon @click.stop="leftDrawer = !leftDrawer" />
      </template>
      <v-app-bar-title>
        {{ currentWife === null ? (currentWife || '老婆名稱') : currentWife }}
      </v-app-bar-title>
      <template v-if="display.width.value < 960">
        <!--icon可變更-->
        <v-btn icon="mdi-information" @click="rightDrawer=!rightDrawer" />
      </template>
    </v-app-bar>

    <v-main style="height: 100vh">
      <v-container class="pa-2" style="height: 100%; overflow-y: scroll">
        <!--chat interface-->
        <div v-if="store.messageMap.get('test 1')">
          <div
            v-for="(message, index) in store.messageMap.get('test 1')"
            :key="index"
            :class="['message-box', message.role]"
          >
            <div class="message-content">
              {{ message.content }}
            </div>
          </div>
        </div>
      </v-container>
    </v-main>
    <v-form @submit.prevent="sendMessage">
      <v-footer app class="pa-0" style="background: none">
        <v-container class="pa-2 pt-0">

          <v-text-field
            v-model="newMessage"
            append-icon="mdi-send"
            density="compact"
            flat
            hide-details
            label="說些什麼吧"
            single-line
            variant="solo"
            @click:append="sendMessage"
          />
        </v-container>
      </v-footer>
    </v-form>

  </v-app>
</template>

<script setup lang="ts">
  import { useAppStore } from '@/stores/app'
  import { useDisplay } from 'vuetify'
  import { useRouter } from 'vue-router'
  import { onMounted, ref, onUnmounted } from 'vue'
  import { broadcast, createWindow } from '@/utils/electronAPI'

  const store = useAppStore()
  const router = useRouter()

  const display = useDisplay()

  // currentWife 定義為一個 ref，這樣它可以是響應式的
  const currentWife = ref<string | null>(null)

   // init value with width
  const windowISUpper500Left = ref(display.width.value >= 750)
  const windowISUpper500Right = ref(display.width.value >= 960)
  const isPermanentLeft = ref(windowISUpper500Left)
  const isPermanentRight = ref(windowISUpper500Right)

  // 控制 navigation drawer 的開關
  const leftDrawer = ref(windowISUpper500Left.value)
  const rightDrawer = ref(windowISUpper500Left.value)

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

  const createNewWife =() => {
    createWindow('/newWife')
}

  // updateCurrentWife 函數來更新 currentWife
  const updateCurrentWife = (Id: string) => {
    currentWife.value = Id
  }

  const goToSettings = () => {
    console.log('Setting')
  }

  const logout = () => {
    store.logout()
    router.push('/')
  }

  // 監聽 window 的 resize 事件，並在 window 尺寸改變時調整 drawer 的狀態
  const windowResizeListener = ref()
  onMounted(() => {
    windowResizeListener.value = window.addEventListener('resize', lefthandleResize)
    windowResizeListener.value = window.addEventListener('resize', righthandleResize)
    lefthandleResize()
    righthandleResize()
  })
  onUnmounted(() => {
    if (windowResizeListener.value !== undefined) {
      window.removeEventListener('resize', windowResizeListener.value)
    }
  })
  const lefthandleResize = () => {
    if (windowISUpper500Left.value && display.width.value < 750) {
      leftDrawer.value = false
      windowISUpper500Left.value = false
      isPermanentLeft.value = false
    } else if (!windowISUpper500Left.value && display.width.value >= 750) {
      leftDrawer.value = true
      windowISUpper500Left.value = true
      isPermanentLeft.value = true
    }
  }
  const righthandleResize = () => {
    if (windowISUpper500Right.value && display.width.value < 960) {
      rightDrawer.value = false
      windowISUpper500Right.value = false
      isPermanentRight.value = false
    } else if (!windowISUpper500Right.value && display.width.value >= 960) {
      rightDrawer.value = true
      windowISUpper500Right.value = true
      isPermanentRight.value = true
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
  background-color: #b2dfdb;
  /* 淺綠色，類似圖中訊息的顏色 */
  border-bottom-right-radius: 0;
}

.message-box.wife .message-content {
  background-color: #e0e0e0;
  /* 灰色，類似圖中對方訊息的顏色 */
  border-bottom-left-radius: 0;
}

.message-role {
  font-weight: bold;
}
</style>
