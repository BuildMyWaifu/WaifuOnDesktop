<template>
    <v-dialog v-model="isDialogOpen" width="500">
        <template v-slot:activator="{props}">
        <v-btn v-bind="props"
        variant="flat">
            <template v-slot:prepend>
            <v-icon icon="mdi-plus"></v-icon>
            </template>
            新增老婆
        </v-btn>
        </template>
        
        <v-container>
            <v-stepper v-model="currentStep" :items="steps" hide-actions>
                <template v-slot:item.1>
                    <v-row dense>
                        <v-col cols="12" md="4" v-for="(companion, index) in wives" :key="index">
                            <v-card variant="plain" @click="selectCard(index)"
                                :class="{ 'selected-card': selectedCard === index }">
                                <v-card-title>{{ companion.name }}</v-card-title>
                                <v-card-text>{{ companion.text }}</v-card-text>
                            </v-card>
                        </v-col>
                    </v-row>
                    <v-card-actions>
                        <v-btn color="primary" @click="prevStep" :disabled="currentStep === 1">
                            上一步
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="nextStep" :disabled="selectedCard === null">
                            下一步
                        </v-btn>
                    </v-card-actions>
                </template>

                <template v-slot:item.2>
                    <v-card class="mx-auto" style="max-width: 500px">
                        <v-form ref="form" v-model="isValid" class="pa-4 pt-6">
                            <v-textarea v-model="name" color="deep-purple" label="name" :rules="[rules.name]"
                                rows="1" variant="filled" auto-grow></v-textarea>
                            <v-textarea v-model="description" color="deep-purple" label="description" :rules="[rules.description]"
                            rows="1" variant="filled" auto-grow></v-textarea>
                            <v-textarea v-model="character" color="deep-purple" label="Character" :rules="[rules.character]"
                                rows="1" variant="filled" auto-grow></v-textarea>
                            <v-textarea v-model="backStory" color="deep-purple" label="BackStory" :rules="[rules.backStory]"
                                rows="1" variant="filled" auto-grow></v-textarea>
                        </v-form>
                        <v-divider></v-divider>
                    </v-card>
                    <v-card-actions>
                        <v-btn color="primary" @click="prevStep" :disabled="currentStep === 1">
                            上一步
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="CloseDialog" :disabled="!isValid">
                            完成
                        </v-btn>
                    </v-card-actions>
                </template>
            </v-stepper>
        </v-container>
    </v-dialog>
</template>

<script lang="ts" setup>
    import { useAppStore } from '@/stores/app';

    const store = useAppStore()

    const isDialogOpen = ref(false)
    const steps = ['新增老婆', '人格構建']
    const currentStep = ref(1)
    const selectedCard = ref(0) // 儲存選擇的卡片索引
    const wives = [
        { name: '老婆1', text: 'filter' },
        { name: '老婆2', text: 'filter' },
        { name: '老婆3', text: 'filter' },
        { name: '老婆4', text: 'filter' },
        { name: '老婆5', text: 'filter' },
        { name: '自定義', text: '' },
    ];

    const isValid = ref(false)
    const name = ref('')
    const description = ref('')
    const character = ref('')
    const backStory = ref('')


    // 點擊卡片時更新選擇的卡片索引
    const selectCard = (index: number) => {
        selectedCard.value = index;
    };
    const rules = {
        name: (value: string) => value === '' ? 'This field is required' : true,
        description: (value: string) => value === '' ? 'This field is required' : true,
        character: (value: string) => value === '' ? 'This field is required' : true,
        backStory: (value: string) => value === '' ? 'This field is required' : true,
        required: (value: boolean) => !!value || 'This field is required',
    };
    const prevStep = () => {
        if (currentStep.value > 1) {
            currentStep.value--
        }
    }
    const nextStep = () => {
        if (currentStep.value < steps.length) {
            currentStep.value++
        }
    }
    const CloseDialog = () => {
        isDialogOpen.value = false
        currentStep.value = 1
    }

</script>

<style scoped>
    .selected-card {
        border: 2px solid #42a5f5;
        /* 選中卡片的邊框顏色 */
        background-color: rgba(66, 165, 245, 0.1);
        /* 選中卡片的背景色 */
    }
</style>