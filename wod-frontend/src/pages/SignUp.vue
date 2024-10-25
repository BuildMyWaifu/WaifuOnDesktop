<template>
  <v-container class="d-flex justify-center align-center h-100 w-100 flex-column">
    <v-card class="mb-4" :loading="loading" style="max-width: 100%;" width="500">
      <v-form v-model="valid" validate-on="input" @submit.prevent="submit">
        <v-card-title class="d-flex text-center justify-center">
          <pre class="d-flex">Build My <div class="text-primary">Waifu</div></pre>
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="payload.email"
            density="compact"
            label="電子郵件"
            :rules="emailRule"
            variant="solo-filled"
          />
          <v-text-field
            v-model="payload.account"
            density="compact"
            label="帳號"
            :rules="rules"
            variant="solo-filled"
          />
          <v-text-field
            v-model="payload.password"
            :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            density="compact"
            label="密碼"
            :rules="passwordRule"
            :type="showPassword ? 'text' : 'password'"
            variant="solo-filled"
            @click:append-inner="showPassword = !showPassword"
          />

          <v-divider />
          <v-card-actions>
            <v-btn
              block
              color="primary"
              dark
              :disabled="!valid"
              :loading="loading"
              type="submit"
            >註冊</v-btn>
          </v-card-actions>
        </v-card-text>
      </v-form>

    </v-card>
    <div class="text-center">
      <div class="text-caption text-info text-decoration-underline" style="cursor: pointer;" @click="toLogIn">
        已經有帳號了嗎？</div>
    </div>
  </v-container>
</template>
<script lang="ts" setup>

  import { ref } from 'vue'
  import { email, password, required } from '@/utils/form'
  import { postApi } from '@/utils/api'
  import { useAppStore } from '@/stores/app'
  import { useRoute, useRouter } from 'vue-router'
  import { hash } from '@/utils/utils'
  import { SubmitEventPromise } from 'vuetify'

  const rules = [required]
  const passwordRule = [required, password]
  const emailRule = [required, email]
  const loading = ref(false)
  const payload = ref({
    email: '',
    account: '',
    password: '',
  })
  const valid = ref(false)
  const showPassword = ref(false)

  const route = useRoute()
  const router = useRouter()
  const appStore = useAppStore()

  async function toLogIn () {
    await router.push({
      path: '/Login',
      query: {
        redirect: route.query.redirect,
      },
    })
  }

  async function submit (event: SubmitEventPromise) {
    loading.value = true
    const results = await event
    if (results.valid) {
      const res = await postApi('/login', {
        account: payload.value.account,
        password: hash(payload.value.password),
      })
      if (res.status === 'success') {
        appStore.login(res.data)

        await router.push('/')
      }
    }
    loading.value = false
  }
</script>
