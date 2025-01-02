<template>

  <div class="d-flex align-center" v-if="localCompanion" style="max-width: 100%;max-height: 100vh;">
    <div class="d-flex justify-center h-100 w-50 align-center overflow-hidden align-center justify-center ">
      <Live2dComponent v-if="localCompanion.live2dModelSettingPath" :fromUrl="localCompanion.live2dModelSettingPath"
        class="h-100 w-100" style="max-height: 100%;max-width: 100%;" :key="randomLive2dKey"></Live2dComponent>
      <div v-else class="flex-grow-1 text-center">無設定模型</div>
    </div>
    <div class="text-start w-50 overflow-y-auto" style="max-height: 100%;">
      <v-card-title class="d-flex align-center flex-wrap">
        {{ localCompanion.name }}


      </v-card-title>
      <v-card-text style="white-space: pre-line;">
        {{ localCompanion.description.replace('\n', '\n\n') }}
      </v-card-text>
      <v-card-title>
        背景故事
      </v-card-title>
      <v-card-text style="white-space: pre-line;">
        {{ localCompanion.backstory.replace('\n', '\n\n') }}
      </v-card-text>
      <v-card-actions v-if="!readonly" style="position: sticky; bottom: 0;background-color: #121212;">
        <v-spacer></v-spacer>
        <v-dialog width="500">
          <template v-slot:activator="{ props }">
            <v-btn v-bind="props" prepend-icon="mdi-delete" color="error" class="mr-4">刪除</v-btn>
          </template>
          <template v-slot:default="{ isActive }">

            <v-card :title="`你確定要刪除「${localCompanion.name}」嗎？`" :subtitle="localCompanion.description">
              
              <v-alert variant="outlined" type="error" icon="mdi-alert" class="mx-4">
                刪除後將無法復原
              </v-alert>
              <v-card-actions class="d-flex justify-space-evenly">
                <v-btn color="success" @click="isActive.value = false">不刪除</v-btn>
                <v-btn color="error" @click="isActive.value = false;deleteCompanion()">刪除</v-btn>
              </v-card-actions>
            </v-card>
          </template>
        </v-dialog>
        <v-divider vertical></v-divider>
        <v-btn v-if="!readonly" :to="`/liveChat/${companionId}`" prepend-icon="mdi-chat" class="ml-4" variant="tonal"
          color="primary">開始聊天</v-btn>
        <v-btn v-if="!readonly" :to="`/companionEdit/${companionId}`" variant="tonal" class="mx-4"
          prepend-icon="mdi-pencil">編輯</v-btn>
      </v-card-actions>
    </div>
  </div>
</template>
<script lang="ts" setup>
  import { useAppStore } from '@/stores/app';
  import Live2dComponent from './Live2dComponent.vue';
  import { computed, PropType, ref } from 'vue';
  import { Companion } from '@/utils/model';
  import { deleteApi } from '@/utils/api';

  const randomLive2dKey = ref(crypto.getRandomValues(new Uint32Array(1))[0].toString(16))

  const props = defineProps({
    companionId: {
      type: String,
    },
    companion: {
      type: Object as PropType<Companion>,
    },
    readonly: {
      type: Boolean,
      default: false,
    }
  })
  const localCompanion = computed(() => {
    if (props.companionId != undefined) {
      return store.getCompanion(props.companionId)
    }
    else {
      return props.companion
    }
  })
  // 在開啟 dialog 之後，透過 copy(companion.value) 來初始化 newCompanion
  const store = useAppStore()
  async function deleteCompanion() {
    const res = await deleteApi(`/companion/${props.companionId}`)
    alert(res.message)
    await store.loadCompanionList()
  }
</script>