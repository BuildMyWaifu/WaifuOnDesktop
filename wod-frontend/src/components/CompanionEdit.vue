<template>
  <v-card v-if="companion">
    <div class="d-flex">
      <div>
        <v-card class="mx-auto" style="max-width: 500px;min-width: 200px;" v-if="companion" variant="flat">
          <v-card-text class="pa-4 pt-10">
            <Live2dComponent :fromFiles="uploadedFiles" v-if="showModel"></Live2dComponent>
            <v-sub-header class="d-flex align-center">僅接受
              <pre class="px-2">.zip</pre> 壓縮檔，關於格式
              <v-dialog width="500">
                <template v-slot:activator="{ props }">
                  <v-icon v-bind="props">mdi-information</v-icon>
                </template>
                <v-card>
                  <v-card-text>
                    <v-card-title>模型格式</v-card-title>
                    <v-card-text>
                      <p>模型檔案必須為壓縮檔，且內含以下檔案：</p>
                      <ul>
                        <li>model.json</li>
                        <li>textures</li>
                      </ul>
                    </v-card-text>
                  </v-card-text>
                </v-card>
              </v-dialog>
            </v-sub-header>
            <v-file-input type="file" accept=".zip" label="上傳新模型" density="compact" @change="handleFileUpload" />
          </v-card-text>
        </v-card>
      </div>
      <div>
        <v-form ref="form" v-model="isValid" class="pa-4 pt-10">
          <v-textarea v-model="companion.profile.name" label="姓名" :rules="[rules.name]" rows="1" variant="filled"
            auto-grow></v-textarea>
          <v-textarea v-model="companion.profile.description" label="描述" :rules="[rules.description]" rows="1"
            variant="filled" auto-grow></v-textarea>
          <v-textarea v-model="companion.prompt.character" label="角色" :rules="[rules.character]" rows="1"
            variant="filled" auto-grow></v-textarea>
          <v-textarea v-model="companion.prompt.backstory" label="背景故事" :rules="[rules.backStory]" rows="1"
            variant="filled" auto-grow></v-textarea>
        </v-form>
      </div>
    </div>


  </v-card>
</template>
<script lang="ts" setup>
  import { Companion } from '@/utils/model';
  import { ref, watch, PropType, onMounted, nextTick } from 'vue';
  import { copy } from '@/utils/utils'
  import Live2dComponent from '@/components/Live2dComponent.vue'

  const isValid = ref(false)
  const showModel = ref(false)

  const props = defineProps({
    modelValue: {
      type: Object as PropType<Companion>,
      required: true
    }
  })

  const emits = defineEmits(['update:modelValue', 'valid-change']);

  const companion = ref<Companion>();

  function reloadModel () {
    showModel.value = false
   nextTick(() => {
      showModel.value = true
    })
  }
  function loadProp() {
    companion.value = copy(props.modelValue)
  }

  onMounted(() => {
    loadProp()
  })
  watch(() => JSON.stringify(props.modelValue), loadProp)
  watch(() => JSON.stringify(companion.value), () => {
    if (companion.value) {
      emits('update:modelValue', copy(companion.value));
    }
  });
  // 當 isValid（表單驗證狀態）改變時，emit 回父層
  watch(isValid, val => {
    emits('valid-change', val);
  });

  const rules = {
    name: (value: string) => value === '' ? '該欄位必須填寫' : true,
    description: (value: string) => value === '' ? '該欄位必須填寫' : true,
    character: (value: string) => value === '' ? '該欄位必須填寫' : true,
    backStory: (value: string) => value === '' ? '該欄位必須填寫' : true,
  };
  const uploadedFiles = ref<File | File[] | null>(null)
  function handleFileUpload(files: File | File[] | null) {
    uploadedFiles.value = files
    reloadModel()
  }



</script>
