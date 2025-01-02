<template>
  <v-card v-if="companion">
    <div class="d-flex px-4 pb-4">
      <div>
        <div class="mx-auto py-4" style="max-width: 500px;min-width: 300px;" v-if="companion">
          <v-card-title>角色模型</v-card-title>
          <v-card-text>


            <Live2dComponent :fromUrl="companion.live2dModelSettingPath" :key="companion.live2dModelSettingPath"
              v-if="showModel && companion.live2dModelSettingPath"></Live2dComponent>
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
              <v-file-input type="file" accept=".zip" label="上傳新的模型（.zip）" density="compact"
                @change="handleLive2dModelUpload" hide-details class="flex-grow-1" />
              <div class="pl-10 text-body-2 pt-1" v-if="companion.live2dModelSettingPath">已經設定好Live2D模型了，可以上傳新模型替代</div>
              <div class="pl-10 text-body-2 pt-1 text-error" v-else>尚未設定Live2D模型</div>
              <div class="d-flex align-center mt-2">
                <v-file-input type="file" accept=".json" label="動作設定（.json）" density="compact" hide-details style="min-width: 230px;"
                  @change="handleUpdateMotionMap" class="flex-grow-1 "></v-file-input>
                <v-btn @click="downloadPoseMap" v-if="companion.poseMap && isNotEmpty(companion.poseMap)"
                  flat>下載動作設定</v-btn>
                <v-menu :close-on-content-click="false">
                  <template v-slot:activator="{ props }">
                    <v-btn flat v-bind="props">預覽動作</v-btn>
                  </template>
                  <v-card>
                    <v-list>
                      <v-list-item v-for="pose, poseKey in companion.poseMap" :key="poseKey"
                        @click="store.doPose(pose)">
                        <v-list-item-title>{{ poseKey }}</v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-card>
                </v-menu>
              </div>
              <div class="pl-10 text-body-2 pt-1" v-if="isNotEmpty(companion.poseMap)">已經設定好動作設定了</div>
              <div class="pl-10 text-body-2 pt-1 text-error" v-else>尚未設定動作設定</div>

            </div>
          </v-card-text>
        </div>
      </div>
      <div class="flex-grow-1 pt-4 pr-4">
        <v-card-title>角色設定</v-card-title>
        <v-form ref="form" v-model="isValid" class="ml-4 flex-gorw-1 ">
          <v-textarea counter v-model="companion.name" label="姓名" :rules="rules.name" rows="1" variant="filled"
            auto-grow></v-textarea>
          <v-textarea counter v-model="companion.description" label="描述" :rules="rules.description" rows="1" variant="filled"
            auto-grow></v-textarea>
          <v-textarea counter v-model="companion.backstory" label="背景故事" :rules="rules.backStory" rows="1" variant="filled"
            auto-grow></v-textarea>
        </v-form>
      </div>
    </div>
  </v-card>
</template>

<script lang="ts" setup>
  import Live2dComponent from "@/components/Live2dComponent.vue";
  import { Companion } from "@/utils/model";
  import { ref, watch, PropType, onMounted, nextTick } from "vue";
  import { copy, isNotEmpty } from "@/utils/utils";
  import { rawPostApi } from "@/utils/api";
  import { saveAs } from 'file-saver';
  import { useAppStore } from "@/stores/app";
import { required } from "@/utils/form";
  // import JSZip from "jszip";
  const store = useAppStore()
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
    name: [required, (v: string) => v.length <= 20 || "名字長度不能超過 20 個字"],
    description: [required, (v: string) => v.length <= 100 || "描述長度不能超過 100 個字"],
    backStory: [required, (v: string) => v.length <= 500 || "角色長度不能超過 500 個字"],
  };
  // 上傳並處理壓縮檔
  async function handleUpdateMotionMap(event: Event) {
    let files = (event.target as HTMLInputElement).files;
    console.log(files)

    if (!files) return;

    let file = undefined as File | undefined;
    if (!(files instanceof File)) {
      file = files[0];
    }
    else {
      file = files;
    }


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
      if (!companion.value) return
      companion.value.poseMap = { ...parsedContent };

    } catch (error) {
      console.error("讀取或解析 JSON 檔案時發生錯誤:", error);
      alert("無法讀取或解析 JSON 檔案");
    }
  }


  async function handleLive2dModelUpload(event: Event) {
    let files = (event.target as HTMLInputElement).files;
    if (!files) return;


    let file = undefined as File | undefined;
    if (!(files instanceof File)) {
      file = files[0];
    }
    else {
      file = files;
    }
    let formData = new FormData

    formData.append('file', file)
    const res = await rawPostApi('/assets/live2dModel/upload', formData)
    if (res.status != 'success') {
      alert(res.message)
      return
    }
    if (!companion.value) return
    companion.value.live2dModelSettingPath = res.data
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


  // 其他現有程式碼...

  function downloadPoseMap() {
    if (!companion.value?.poseMap) {
      alert("poseMap is not available or is empty.");
      return;
    }

    try {
      const blob = new Blob([JSON.stringify(companion.value.poseMap, null, 2)], { type: 'application/json' });
      saveAs(blob, 'poseMap.json');
    } catch (error) {
      console.error("Error downloading poseMap:", error);
      alert("An error occurred while trying to download the poseMap.");
    }
  }
</script>