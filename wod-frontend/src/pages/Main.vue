<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <v-navigation-drawer app location="left" permanent>

      <v-list lines="two" select-strategy="single-independent" width="256">

        <v-list-item v-show="store.companionList == undefined">
          <v-card-text class="d-flex text-center">
            載入伴侶列表中
          </v-card-text>
        </v-list-item>

        <v-list-item v-show="store.companionList != undefined && store.companionList.length == 0">
          <v-card-text class="d-flex text-center">
            伴侶列表為空
          </v-card-text>
        </v-list-item>
        <template v-for="companion in store.companionList" :key="companion._id">

          <v-list-item :value="companion._id" @click="updateCurrentCompanion(companion._id)">
            <v-list-item-title>{{ companion.name }}</v-list-item-title>
            <v-list-item-subtitle class="text-caption">{{ companion.description }}</v-list-item-subtitle>
            <div class="text-body-2" v-if="store.messageMap.get(companion._id) && lastMessage(companion._id)">
              {{ lastMessage(companion._id)?.role == 'assistance' ? companion.name : '您' }}：{{
                lastMessage(companion._id)?.content }}
            </div>
          </v-list-item>
          <v-divider />
        </template>

      </v-list>

      <div class="px-4">
        <v-btn variant="outlined" block color="primary" prepend-icon="mdi-plus" to="/createNewWaifu">
          新增伴侶
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
                <UserSettingListItem />
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

    <v-main app>
      <CompanionPreview style="height: 100vh; max-height: 100vh;" v-if="currentCompanionId !== null"
      :companionId="currentCompanionId" :key="currentCompanionId"></CompanionPreview>

    </v-main>

  </v-app>
</template>

<script setup lang="ts">

  import CompanionPreview from '@/components/CompanionPreview.vue'
  import UserSettingListItem from '@/components/UserSettingListItem.vue';
  import { useAppStore } from '@/stores/app';
  import { useRouter, useRoute } from 'vue-router';
  import { ref, onMounted } from 'vue';

  const store = useAppStore();
  const router = useRouter();
  const route = useRoute()
  const currentCompanionId = ref<string | null>(null);


  // 新增訊息內容的變數

  const lastMessage = (Id: string) => {
    const messages = store.messageMap.get(Id)
    return messages ? messages[messages.length - 1] : undefined
  }
  // updateCurrentCompanion 函數來更新 currentCompanion
  const updateCurrentCompanion = (Id: string) => {
    currentCompanionId.value = Id; // 切換到新的
  }
  const logout = () => {
    store.logout()
    router.push('/')
  }

  // 監聽 window 的 resize 事件，並在 window 尺寸改變時調整 drawer 的狀態
  onMounted(async () => {
    await store.loadCompanionList()
    if (store.companionList != undefined && store.companionList.length != 0) {
      currentCompanionId.value = store.companionList[0]._id
    }
    if ('companionId' in route.params) {
      currentCompanionId.value = route.params.companionId as string
    }

  })

</script>

<style scoped></style>
