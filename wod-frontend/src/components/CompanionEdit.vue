<template>
  <v-card v-if="companion">
    <div class="d-flex">
      <div>
        <div class="mx-auto pa-4" style="max-width: 500px;min-width: 200px;" v-if="companion">
          <v-card-title>角色模型</v-card-title>
          <!-- <Live2dComponent :fromFiles="uploadedFiles" v-if="showModel"></Live2dComponent> --> <v-container>
            <div style="max-height: 50vh;" class="overflow-y-auto">

              <div v-for="(url, index) in imageUrls" :key="index">
                <v-img :src="url" class="ma-2" aspect-ratio="1.5" />
              </div>
            </div>
          </v-container>
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

        </div>
      </div>
      <div class="flex-grow-1 pt-4 pr-4">
        <v-card-title>角色設定</v-card-title>
        <v-form ref="form" v-model="isValid" class="pa-4 pt-10 flex-gorw-1 overflow-y-auto " style="max-height: 60vh;">
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
  import { Companion } from "@/utils/model";
  import { ref, watch, PropType, onMounted, nextTick } from "vue";
  import { copy } from "@/utils/utils";
  import JSZip from "jszip";

  const isValid = ref(false);
  const showModel = ref(false);
  const imageUrls = ref<string[]>([]); // 用於存儲圖片的 URL

  const props = defineProps({
    modelValue: {
      type: Object as PropType<Companion>,
      required: true,
    },
  });

  const emits = defineEmits(["update:modelValue", "valid-change"]);

  const companion = ref<Companion>();

  function reloadModel() {
    showModel.value = false;
    nextTick(() => {
      showModel.value = true;
    });
  }
  function loadProp() {
    companion.value = copy(props.modelValue);
  }

  onMounted(() => {
    loadProp();
  });
  watch(() => JSON.stringify(props.modelValue), loadProp);
  watch(
    () => JSON.stringify(companion.value),
    () => {
      if (companion.value) {
        emits("update:modelValue", copy(companion.value));
      }
    }
  );
  // 當 isValid（表單驗證狀態）改變時，emit 回父層
  watch(isValid, (val) => {
    emits("valid-change", val);
  });

  const rules = {
    name: (value: string) => (value === "" ? "該欄位必須填寫" : true),
    description: (value: string) => (value === "" ? "該欄位必須填寫" : true),
    character: (value: string) => (value === "" ? "該欄位必須填寫" : true),
    backStory: (value: string) => (value === "" ? "該欄位必須填寫" : true),
  };
  const uploadedFiles = ref<File | File[] | null>(null);

  // 上傳並處理壓縮檔
  async function handleFileUpload(event: Event) {
    let files = (event.target as HTMLInputElement).files;


    if (files && !(files instanceof File)) {
      files = files[0];
    }
    if (!files) return;
    uploadedFiles.value = files;
    console.log("Start to handle file upload");
    console.log(files);

    const zip = new JSZip();
    const content = await zip.loadAsync(files);
    imageUrls.value = []; // 清空已有的圖片

    for (const [fileName, fileData] of Object.entries(content.files)) {
      // alert(fileName);
      if (/\.(png|jpe?g|gif)$/i.test(fileName) && !fileData.dir) {
        const blob = await fileData.async("blob");
        const url = URL.createObjectURL(blob);
        imageUrls.value.push(url);
      }
    }

    reloadModel();
  }
</script>