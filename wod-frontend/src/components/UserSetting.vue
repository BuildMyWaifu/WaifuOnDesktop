<!-- eslint-disable vue/valid-v-slot -->
<template>
    <v-dialog v-model="isDialogOpen" max-width="500" @update:modelValue="onDialogClose">
        <v-card>
            <v-card-title class="text-h5">
                <v-row class="align-center">
                    <v-col>設定</v-col>
                    <v-col class="text-end">
                        <v-btn icon="mdi-close" @click="closeDialog" />
                    </v-col>
                </v-row>
            </v-card-title>
            <v-card-text>
                <div>這是設定內容</div>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup>
    import { ref } from 'vue';

    // 接收父組件的 @close 事件
    const emits = defineEmits(['close']);
    const isDialogOpen = ref(true);

    // 關閉對話框
    const closeDialog = () => {
    isDialogOpen.value = false; // 關閉對話框
    emits('close');
    };

    // 監聽對話框關閉事件
    const onDialogClose = (value: boolean) => {
    if (!value) {
        emits('close');
    }
    };
</script>
