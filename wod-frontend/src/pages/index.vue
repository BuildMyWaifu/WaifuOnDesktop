<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto" max-width="900">
      <div class="text-center">
        <div class="text-h3 font-weight-light mb-n1">Build My</div>

        <h1 class="text-h2 font-weight-bold text-primary">Waifu</h1>
      </div>

      <div class="py-4" />
      <div v-if="auth" class="d-flex justify-center">
        <v-btn class="ma-3" to="/app" variant="outlined">進入</v-btn>
        <v-btn class="ma-3" to="/app" variant="outlined">進入錯誤頁面</v-btn>
      </div>
      <div v-else class="d-flex justify-center">
        <v-alert style="max-width: 500px;" type="warning" variant="tonal">
          您還未登入！
          <template #append>
            <router-link class="pr-4 text-grey" to="login">登入</router-link>
            <router-link class=" text-grey" to="signup">註冊</router-link>
          </template>
        </v-alert>

      </div>
      <v-card style="position: fixed; right: 8px; bottom: 8px">
        <v-card-text>
          <v-btn variant="text" @click="toggleAuthStat">切換登入狀態</v-btn>

        </v-card-text>
      </v-card>
    </v-responsive>
  </v-container>
</template>

<script lang="ts" setup>
  import { useAppStore } from '@/stores/app'

  const store = useAppStore()
  const auth = computed(() => {
    if (store.user !== undefined) {
      return true
    }
    return false
  })
  function toggleAuthStat () {
    if (store.user !== undefined) {
      store.logout()
    } else {
      store.login({ _id: 'test', profile: { avatarId: 'test avatarId', name: 'test name', email: 'test' } })
    }
  }
</script>
