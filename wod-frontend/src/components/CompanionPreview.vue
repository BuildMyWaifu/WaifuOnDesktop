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
        <v-btn v-if="!readonly" :to="`/liveChat/${companionId}`" prepend-icon="mdi-chat" class="ml-4"
          color="primary">開始聊天</v-btn>
        <v-dialog max-width="500">
          <template v-slot:activator="{ props: activatorProps }">
            <v-btn v-bind="activatorProps" variant="text" class="mx-4" prepend-icon="mdi-pencil">編輯</v-btn>
          </template>

          <template v-slot:default="{ isActive }">
            <v-card title="編輯角色">
              <v-card-text>
                這是一個dialog
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn text="關閉" @click="isActive.value = false"></v-btn>
              </v-card-actions>
            </v-card>
          </template>
        </v-dialog>
      </v-card-actions>
    </div>
  </div>
</template>
<script lang="ts" setup>
  import { useAppStore } from '@/stores/app';
  import Live2dComponent from './Live2dComponent.vue';

  import { computed, PropType, ref } from 'vue';
  import { Companion } from '@/utils/model';

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

</script>