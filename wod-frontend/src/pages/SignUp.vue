<template>
  <v-container class="d-flex justify-center align-center h-100 w-100 flex-column">
    <v-card class="mb-4" :loading="loading" style="max-width: 100%;" width="500">
      <v-form v-model="formValid" validate-on="input" @submit.prevent="submitSignUp">
        <v-card-title class="d-flex text-center justify-center">
          <LogoText></LogoText>
        </v-card-title>
        <v-card-text class="pb-0">
          <v-text-field flat  v-model="payload.email" density="compact" label="電子郵件" :rules="[email, required]"
            variant="solo-filled" />
          <v-text-field flat  v-model="payload.name" density="compact" label="帳號" :rules="[name, required]"
            variant="solo-filled" />
          <v-text-field  flat v-model="payload.password" :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            density="compact" label="密碼" :rules="[password, required]" :type="showPassword ? 'text' : 'password'"
            variant="solo-filled" @click:append-inner="showPassword = !showPassword" />

          <v-divider />
        </v-card-text>
        <v-card-actions>
          <div class="d-flex justify-center w-100">
            <v-btn
              block
              color="primary"
              :disabled="!formValid"
              :loading="loading"
              type="submit"
            >註冊</v-btn>
          </div>
        </v-card-actions>
      </v-form>

    </v-card>
    <div class="text-center d-flex">
      <div class="text-caption text-info text-decoration-underline pr-4" style="cursor: pointer;"
        @click="() => { router.push('/') }">
        返回首頁</div>
      <div class="text-caption text-info text-decoration-underline" style="cursor: pointer;" @click="redirectToLogin">
        已經有帳號了嗎？</div>
    </div>
    <v-snackbar v-model="showSnackBar" :color="snackbar?.status">{{ snackbar?.message }}</v-snackbar>
  </v-container>
</template>
<script lang="ts" setup>
  import { ref } from 'vue'
  import { postApi, fetchApi } from '@/utils/api'
  import { useAppStore } from '@/stores/app'
  import { useRoute, useRouter } from 'vue-router'
  import { email, name, password, required } from '@/utils/form'
  import { hash } from '@/utils/utils'
  import { SubmitEventPromise } from 'vuetify'
  import { electronStoreSet } from '@/utils/electronAPI'
  import LogoText from '@/components/LogoText.vue'

  const store = useAppStore()
  const router = useRouter()
  const loading = ref(false)
  const formValid = ref(false)
  const payload = ref({
    name: '',
    email: '',
    password: '',
  })
  const showPassword = ref(false)
  const snackbar = ref<{ status: string, message: string }>()
  const showSnackBar = ref(false)
  const route = useRoute()

  const redirectToLogin = () => {
    router.push('/login')
  }
  async function submitSignUp(event: SubmitEventPromise) {
    loading.value = true
    const results = await event
    if (results.valid) {
      let res = await postApi('/signup', {
        name: payload.value.name,
        email: payload.value.email,
        password: hash(payload.value.password),
      })
      snackbar.value = res
      showSnackBar.value = true
      if (res.status === 'success') {
        await electronStoreSet('token', res.data)
        res = await fetchApi('/me')
        await store.login(res.data)
        const redirectPath = route.query.redirect
        if (redirectPath) {
          await router.push(redirectPath.toString())
        } else {
          await router.push('/app')
        }
      }
    }
    loading.value = false
  }
</script>