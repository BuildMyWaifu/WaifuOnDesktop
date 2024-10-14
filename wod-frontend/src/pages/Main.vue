<template>
  <v-app>
    <v-app-bar>
      <template v-slot:prepend>
        <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      </template>
      <v-app-bar-title>
        {{ currentWife === null ? (currentWife || '老婆名稱') : currentWife }}
      </v-app-bar-title>
    </v-app-bar>

    <v-navigation-drawer location="left" v-model="drawer" app>
      <v-list lines="three" select-strategy="single-independent">
        <template #prepend>
          <v-avatar />
        </template>
        <v-list-item v-for="companion in store.companionList" :key="companion._id" :value="companion._id" @click="updateCurrentWife(companion._id)">
          <v-list-item-title>{{ companion._id }}</v-list-item-title>
          <v-list-item-subtitle>
            <div v-if="store.messageMap.get(companion._id)">
              {{ lastMessage(companion._id)?.content || 'No messages yet' }}
            </div>
          </v-list-item-subtitle>
        </v-list-item>
        <v-divider></v-divider>
      </v-list>
      <template #append>
        <v-divider></v-divider>
        <v-list-item v-if="store.user" lines="three">
          <v-list-item-title>
            {{ store.user?.profile.name }}
          </v-list-item-title>

          <template v-slot:append>
            <v-menu offset-y>
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props"  position="sticky">
                  ...
                </v-btn>
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

    <v-main>
      <v-container style="max-height: 80vh; overflow: auto">
        chat interface
        <pre><code>{{ store.messageMap }}</code></pre>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
  import { useAppStore } from '@/stores/app'

  const store = useAppStore()
  const router = useRouter();

  // 控制 navigation drawer 的開關
  const drawer = ref(false); // 初始為 false，即隱藏

  // currentWife 定義為一個 ref，這樣它可以是響應式的
  const currentWife = ref<string | null>(null);

  const lastMessage = (Id: string) => {
    const messages = store.messageMap.get(Id);
    return messages ? messages[messages.length - 1] : null;
}
  
  // updateCurrentWife 函數來更新 currentWife
  const updateCurrentWife = (Id: string) => {
    currentWife.value = Id;
  };

  const goToHome = () => {
    router.push('/');
  };

  const goToSettings = () => {
    console.log('Setting');
  };

  const logout = () => {
    console.log('Logging out...');
  };
</script>
