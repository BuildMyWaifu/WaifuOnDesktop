<template>
    <v-card class="mx-auto" style="max-width: 500px" v-if="companion">
        <div class="d-flex">
            <div class="pa-4 pt-10 text-center">
                <label style="font-size: 14px; display: block; margin-bottom: 10px;">avatar here </label>
                <!-- Custom upload button -->
                <div style="margin-top: 20px; text-align: center;">
                    <div style="position: relative;">
                        <input type="file" accept="image/jpeg, image/png, video/mp4" @change="handleFileUpload" style="
                            position: absolute;
                            opacity: 0;
                            width: 100%;
                            height: 100%;
                            cursor: pointer;
                            z-index: 1;
                            " />
                        <button style="
                            display: block;
                            width: 100%;
                            padding: 12px 20px;
                            font-size: 14px;
                            border: none;
                            border-radius: 8px;
                            background: linear-gradient(120deg, #9b59b6, #8e44ad);
                            color: white;
                            cursor: pointer;
                            text-align: center;
                            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                            transition: transform 0.2s ease, box-shadow 0.2s ease;
                            z-index: 2;
                            " @mouseover="handleMouseOver" @mouseleave="handleMouseLeave">
                            上傳模型
                        </button>
                    </div>
                </div>
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

    const props = defineProps({
        modelValue: {
            type: Object as PropType<Companion>,
            required: true
        }
    })

    const emits = defineEmits(['update:modelValue'])

    const companion = ref<Companion>();
    function loadProp() {

        companion.value = copy(props.modelValue)
    }
    onMounted(() => {
        loadProp()
    })
    watch(() => JSON.stringify(props.modelValue), loadProp)
    watch(() => JSON.stringify(companion.value), () => {
        emits('update:modelValue', copy(companion.value));
    });

    const rules = {
        name: (value: string) => value === '' ? '該欄位必須填寫' : true,
        description: (value: string) => value === '' ? '該欄位必須填寫' : true,
        character: (value: string) => value === '' ? '該欄位必須填寫' : true,
        backStory: (value: string) => value === '' ? '該欄位必須填寫' : true,
    };

    // Handle user-uploaded
    const handleFileUpload = (event: Event) => {
        // 確保 event.target 是 HTMLInputElement
        const input = event.target as HTMLInputElement;
        const file = input.files?.[0]; // 使用可選鏈接

        if (!file) return;

        input.value = ''; // Clear the input value for re-uploading the same file
    };

    const handleMouseOver = (event: MouseEvent) => {
        const target = event.target as HTMLButtonElement;
        if (target) {
            target.style.transform = 'scale(1.05)';
        }
    };

    const handleMouseLeave = (event: MouseEvent) => {
        const target = event.target as HTMLButtonElement;
        if (target) {
            target.style.transform = 'scale(1)';
        }
    };

</script>
