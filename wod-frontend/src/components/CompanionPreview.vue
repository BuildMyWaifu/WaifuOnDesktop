<template>


  <v-container>
    <v-row>
      <v-col cols="6">
        <Live2dComponent></Live2dComponent>
      </v-col>
      <v-col cols="6" class="text-center">
        <v-card-title class="text-h5">
          {{ localCompanion.profile.name }}
        </v-card-title>
        <v-card-text class="text-h7">
          {{ localCompanion.profile.description }}
        </v-card-text>


        <v-container>
          <v-card-title class="text-h6">
            性格
          </v-card-title>
          <v-card-text class="text-h7" style="border: 1px solid #ccc; border-radius:10px; padding: 16px;">
            {{ localCompanion.prompt.character }}
          </v-card-text>
        </v-container>

        <v-container>
          <v-card-title class="text-h">
            背景設定
          </v-card-title>
          <v-card-text class="text-h7" style="border: 1px solid #ccc; border-radius:10px; padding: 16px;">
            {{ localCompanion.prompt.backstory }}
          </v-card-text>
        </v-container>

        <v-dialog max-width="500" v-if="!readonly">
          <template v-slot:activator="{ props: activatorProps }">
            <v-btn v-bind="activatorProps" color="surface-variant" text="編輯" variant="flat" class="ma-4"></v-btn>
            <v-btn color="surface-variant" text="確定選擇" variant="flat" class="ma-4"></v-btn>
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

      </v-col>

    </v-row>
  </v-container>



</template>
<script lang="ts" setup>
  import { useAppStore } from '@/stores/app';
  import Live2dComponent from './Live2dComponent.vue';

  import { computed, PropType } from 'vue';
  import { Companion } from '@/utils/model';

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