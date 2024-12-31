<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-container class="d-flex justify-center align-center h-100 w-100 flex-column">
    <v-card class="mb-4" :loading="loading" style="max-width: 100%;" width="500">
      <v-form v-model="valid" validate-on="input" @submit.prevent="submit">
        <v-card-title class="d-flex text-center justify-center">
          <pre class="d-flex">Build My <div class="text-primary">Waifu</div></pre>
        </v-card-title>
        <v-card-text>
          <v-text-field v-model="payload.email" density="compact" label="電子郵件" :rules="rules" variant="solo-filled" />
          <v-text-field v-model="payload.password" :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            density="compact" label="密碼" :rules="rules" :type="showPassword ? 'text' : 'password'" variant="solo-filled"
            @click:append-inner="showPassword = !showPassword" />

          <v-divider />
          <v-card-actions>
            <v-btn block color="primary" dark :disabled="!valid" :loading="loading" type="submit">登入</v-btn>
          </v-card-actions>
        </v-card-text>
      </v-form>

    </v-card>
    <div class="text-center d-flex">
      <div class="text-caption text-info text-decoration-underline pr-4" style="cursor: pointer;"
        @click="() => { router.push('/') }">
        返回首頁</div>
      <div class="text-caption text-info text-decoration-underline" style="cursor: pointer;" @click="toSignUp">
        沒有帳號嗎？</div>
    </div>
    <v-snackbar v-model="showSnackBar" :color="snackbar?.status">{{ snackbar?.message }}</v-snackbar>
  </v-container>
</template>
<script lang="ts" setup>

  import { ref } from 'vue'
  import { required } from '@/utils/form'
  import { postApi, fetchApi } from '@/utils/api'
  import { useAppStore } from '@/stores/app'
  import { useRoute, useRouter } from 'vue-router'
  import { hash } from '@/utils/utils'
  import { SubmitEventPromise } from 'vuetify'
  import { electronStoreSet } from '@/utils/electronAPI'

  const rules = [required]
  const loading = ref(false)
  const payload = ref({
    email: '',
    password: '',
  })
  const valid = ref(false)
  const showPassword = ref(false)
  const snackbar = ref<{ status: string, message: string }>()
  const showSnackBar = ref(false)

  const route = useRoute()
  const router = useRouter()
  const appStore = useAppStore()

  async function toSignUp() {
    await router.push({
      path: '/signup',
      query: {
        redirect: route.query.redirect,
      },
    })
  }

  async function submit(event: SubmitEventPromise) {
    loading.value = true
    const results = await event
    if (results.valid) {
      const tokenRes = await postApi('/login', {
        email: payload.value.email,
        password: hash(payload.value.password),
      })
      if (!tokenRes) {
        snackbar.value = {
          status: 'error',
          message: '登入失敗',
        }
        showSnackBar.value = true
        return
      }
      const token = tokenRes.data
      await electronStoreSet('token', token)
      const res = await fetchApi("/me")
      snackbar.value = res
      showSnackBar.value = true
      if (res.status === 'success') {
        await appStore.login(res.data)
        await router.push('/app')
      }
    }
    loading.value = false
  }
</script>
