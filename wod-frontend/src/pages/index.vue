<!-- eslint-disable vue/multi-word-component-names -->
<!-- eslint-disable-next-line vue/multi-word-component-names -->
<template>
  <v-container class="fill-height">
    <v-responsive class="align-center fill-height mx-auto" max-width="900">
      <div class="text-center text-h1 pb-1">
        <v-img height="240" src="@/assets/logo.png" />
      </div>
      <div class="text-center text-h5">
        一個屬於你的動態伴侶陪伴神器
      </div>
      <div class="py-2" />
      <div class="text-center">
        <v-dialog width="600">
          <template v-slot:activator="{ props }">
            <v-btn v-bind="props" prepend-icon="mdi-message" color="error" variant="outlined">
              給助教的重要訊息
            </v-btn>
          </template>
          <v-card title="關於額度">
            <v-card-text>
              <div class="mb-3">
                由於本系統 LLM 相關費用由學生（我們）自掏腰包承擔，為了避免過高的費用支出，現在所有帳號可用次數總共為 300 次。 <br>
              </div>
              <div class="mb-3">
                而助教或是教授如需測試，請使用助教帳號登入，該帳號擁有獨立的 300 次可用額度。 <br>
              </div>
              助教帳號：

              <pre><code>帳號：jason5******@gmail.com（軟體工程李助教的電子郵件）
密碼：Abcd1234</code></pre>

            </v-card-text>
          </v-card>
        </v-dialog>
      </div>
      <div class="py-1" />

      <div v-if="auth" class="d-flex justify-center">
        <v-btn class="ma-3" to="/app" variant="outlined">進入</v-btn>

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
    </v-responsive>
  </v-container>
</template>

<script lang="ts" setup>
  import { useAppStore } from '@/stores/app'
  import { computed } from 'vue';

  const store = useAppStore()
  const auth = computed(() => {
    if (store.user !== undefined) {
      return true
    }
    return false
  })

</script>
