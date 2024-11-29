<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <v-navigation-drawer v-model="leftDrawer" app location="left" :permanent="isPermanentLeft">
      <v-list lines="two" select-strategy="single-independent">
        <template #prepend>
          <v-avatar /> <!-- avatar for Companion -->
        </template>
        <v-list-item v-for="companion in store.companionList" :key="companion._id" :value="companion._id"
          @click="updateCurrentCompanion(companion._id)">
          <v-list-item-title>{{ companion.profile.name }}</v-list-item-title>
          <v-list-item-subtitle class="text-caption">{{ companion.profile.description }}</v-list-item-subtitle>
          <div class="text-body-2" v-if="store.messageMap.get(companion._id) && lastMessage(companion._id)">
            {{ lastMessage(companion._id)?.role == 'bot' ? companion.profile.name : '您' }}：{{
              lastMessage(companion._id)?.content }}
          </div>
        </v-list-item>
        <v-divider />
      </v-list>
      <div class="text-center">
        <CreateNewWife />
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
        <v-list-item v-else>
          <v-list-item-title>
            目前尚未登入
          </v-list-item-title>
          <v-list-item-subtitle>
            <v-btn to="/login">登入</v-btn>
          </v-list-item-subtitle>
        </v-list-item>
      </template>
    </v-navigation-drawer>

    <CompanionPreview
      v-if="currentCompanionId !== null" :companionId="currentCompanionId"></CompanionPreview>
    <!-- <v-app-bar elevation="0">
      <template v-if="display.width.value < 750">
        <v-app-bar-nav-icon @click.stop="leftDrawer = !leftDrawer" />
      </template>
      <v-app-bar-title>
        {{ currentCompanionId === null ? (currentCompanionId || '老婆名稱') : currentCompanionId }}
      </v-app-bar-title>
      <template v-if="display.width.value < 960">
        <v-btn icon="mdi-information" @click="rightDrawer = !rightDrawer" />
      </template>
    </v-app-bar>
    <ChatInterface v-if="currentCompanionId !== null" :companionId="currentCompanionId" /> -->
  </v-app>
</template>

<script setup lang="ts">
  import CompanionDrawer from '@/components/CompanionDrawer.vue'
  import CompanionPreview from '@/components/CompanionPreview.vue'
  import ChatInterface from '@/components/ChatInterface.vue'
  import CreateNewWife from '@/components/CreateNewWife.vue'

  import { useAppStore } from '@/stores/app'
  import { useDisplay } from 'vuetify'
  import { useRouter } from 'vue-router'
  import { onMounted, ref, onUnmounted } from 'vue'

  const store = useAppStore()
  const router = useRouter()

  const display = useDisplay()
  const currentCompanionId = ref<string | null>(null)

  const windowISUpper500Left = ref(display.width.value >= 750)
  const windowISUpper500Right = ref(display.width.value >= 960)
  const isPermanentLeft = ref(windowISUpper500Left)
  const isPermanentRight = ref(windowISUpper500Right)

  // 控制 navigation drawer 的開關
  const leftDrawer = ref(windowISUpper500Left.value)
  const rightDrawer = ref(windowISUpper500Left.value)

  // 新增訊息內容的變數

  const lastMessage = (Id: string) => {
    const messages = store.messageMap.get(Id)
    return messages ? messages[messages.length - 1] : undefined
  }
  // updateCurrentCompanion 函數來更新 currentCompanion
  const updateCurrentCompanion = (Id: string) => {
    currentCompanionId.value = Id
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
    currentCompanionId.value = store.companionList[0]._id
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

<style scoped></style>
