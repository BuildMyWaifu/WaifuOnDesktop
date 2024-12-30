<template>
    <v-card class="mx-auto" style="max-width: 500px" v-if="companion">
        <div class="d-flex">
            <div>
                <v-card class="mx-auto" style="max-width: 500px" v-if="companion" variant="flat">
                    <v-card-text class="pa-4 pt-10" style="text-align: center">模型在此</v-card-text>
                    <v-card-text class="pa-4 pt-10">
                        <v-btn color="primary" @click="openFileDialog">
                            上傳模型
                        </v-btn>

                        <!-- 隱藏起來的 v-file-input -->
                        <v-file-input
                            ref="fileInput"
                            accept="image/jpeg, image/png, video/mp4"
                            style="display: none"
                            @change="handleFileUpload"
                        />
                    </v-card-text>
                    <!-- 其他表單欄位... -->
                </v-card>
            </div>
            <div>
                <v-form ref="form" v-model="isValid" class="pa-4 pt-10">
                    <v-textarea v-model="companion.profile.name" label="姓名" :rules="[rules.name]" rows="1"
                        variant="filled" auto-grow></v-textarea>
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
    import { ref, watch, PropType, onMounted } from 'vue';
    import { copy } from '@/utils/utils'

    const isValid = ref(false)
    const fileInput = ref() // 拿來存放對 v-file-input 的引用

    const props = defineProps({
        modelValue: {
            type: Object as PropType<Companion>,
            required: true
        }
    })

    const emits = defineEmits(['update:modelValue', 'valid-change']);

    const companion = ref<Companion>();

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

    function openFileDialog() {
    // 透過 ref 拿到 v-file-input 元件，然後找到它內部的 <input type="file">，手動觸發 click
    const el = fileInput.value?.$el as HTMLElement | undefined
    el?.querySelector('input')?.click()
    }

    function handleFileUpload(files: File | File[] | null) {
    // 這裡就是 v-file-input 上傳完檔案後會觸發的事件
    // files 可能是單檔或多檔 (若你有用 multiple)
    console.log(files)
    }

    

</script>
