<template>
  <v-app>

    <v-navigation-drawer>
      <v-list three-line>
        <template #prepend>
          <v-avatar />
        </template>
        <v-list-item>
          <v-list-item-title>老婆一號</v-list-item-title>
          <v-list-item-subtitle>老婆一號：你好呀！呀！呀！呀！呀！</v-list-item-subtitle>
        </v-list-item>
      </v-list>
      <template #append>
        <div class="d-flex justify-center">
          <router-link class="text-grey" to="/">
            回到主頁面
          </router-link>
        </div>
        <div class="d-flex">
          <v-spacer />
          <v-btn stacked>設定</v-btn>
          <v-btn stacked>登出</v-btn>
        </div>
        <v-list-item v-if="store.user" lines="three">
          <v-list-item-title>
            {{ store.user?.profile.name }}
          </v-list-item-title>
        </v-list-item>
      </template>
    </v-navigation-drawer>
    <v-app-bar>
      老婆名稱
    </v-app-bar>
    <v-main>
      chat interface
    </v-main>
  </v-app>
</template>
<script setup lang="ts">
  import { useAppStore } from '@/stores/app'

  const store = useAppStore()

</script>
