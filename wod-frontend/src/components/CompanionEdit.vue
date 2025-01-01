<template>
  <v-card v-if="companion">
    <div class="d-flex">
      <div>
        <div class="mx-auto pa-4" style="max-width: 500px;min-width: 300px;" v-if="companion">
          <v-card-title>角色模型</v-card-title>
          <Live2dComponent :fromUrl="modelUrl" :key="modelUrl" v-if="showModel"></Live2dComponent>
          <!-- 材質預覽 -->
          <!-- <v-container>
            <div style="max-height: 50vh;" class="overflow-y-auto">

              <div v-for="(url, index) in imageUrls" :key="index">
                <v-img :src="url" class="ma-2" aspect-ratio="1.5" />
              </div>
            </div>
          </v-container> -->
          <div class="d-flex align-center text-grey mt-2">關於格式
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
          </div>
          <div class="mt-2">
            <v-file-input type="file" accept=".zip" label="上傳新模型（.zip）" density="compact" @change="handleFileUpload"
              hide-details class="flex-grow-1" />
            <v-file-input type="file" accept=".json" label="動作設定（.json）" density="compact" hide-details @change="handleUpdateMotionMap"
              class="flex-grow-1 mt-2"></v-file-input>
          </div>

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
  import Live2dComponent from "@/components/Live2dComponent.vue";
  import { Companion } from "@/utils/model";
  import { ref, watch, PropType, onMounted, nextTick } from "vue";
  import { copy } from "@/utils/utils";
  import { rawPostApi } from "@/utils/api";
  // import JSZip from "jszip";

  const isValid = ref(false);
  const showModel = ref(true);
  // const imageUrls = ref<string[]>([]); // 用於存儲圖片的 URL

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
    reloadModel();
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
  const modelUrl = ref<string | null>(null);
  // 上傳並處理壓縮檔

  const motionMap = ref<{ [key: string]: string}>()

  async function handleUpdateMotionMap(event: Event) {
    let files = (event.target as HTMLInputElement).files;

    if (files && !(files instanceof File)) {
      files = files[0];
    }
    if (!files) return;

    const file = files;

    if (file.type !== "application/json") {
      alert("請上傳有效的 JSON 檔案");
      return;
    }

    try {
      // 讀取檔案內容
      const fileContent = await file.text();

      // 將 JSON 內容解析為物件
      const parsedContent = JSON.parse(fileContent);

      if (typeof parsedContent !== "object" || Array.isArray(parsedContent)) {
        alert("上傳的 JSON 檔案格式不正確");
        return;
      }

      // 更新 motionMap.value
      motionMap.value = { ...parsedContent };

    } catch (error) {
      console.error("讀取或解析 JSON 檔案時發生錯誤:", error);
      alert("無法讀取或解析 JSON 檔案");
    }
  }


  async function handleFileUpload(event: Event) {
    let files = (event.target as HTMLInputElement).files;


    if (files && !(files instanceof File)) {
      files = files[0];
    }
    if (!files) return;
    let formData = new FormData

    formData.append('file', files)
    const res = await rawPostApi('/assets/live2dModel/upload', formData)
    if (res.status != 'success') {
      alert(res.message)
      return
    }
    modelUrl.value = res.data
    // const zip = new JSZip();
    // const content = await zip.loadAsync(files);
    // imageUrls.value = []; // 清空已有的圖片

    // for (const [fileName, fileData] of Object.entries(content.files)) {
    //   // alert(fileName);
    //   if (/\.(png|jpe?g|gif)$/i.test(fileName) && !fileData.dir) {
    //     const blob = await fileData.async("blob");
    //     const url = URL.createObjectURL(blob);
    //     imageUrls.value.push(url);
    //   }
    // }

    reloadModel();
  }
</script>