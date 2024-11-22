<!-- <v-stepper-actions> 尚未處理-->
<template>
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
                        <v-textarea v-model="character" color="deep-purple" label="Character" :rules="[rules.character]"
                            rows="1" variant="filled" auto-grow></v-textarea>
                        <v-textarea v-model="backStory" color="deep-purple" label="BackStory" :rules="[rules.backStory]"
                            rows="1" variant="filled" auto-grow></v-textarea>
                        <v-checkbox v-model="agreement" :rules="[rules.required]" color="deep-purple">
                            <template v-slot:label>
                                I agree to the&nbsp;
                                <a href="#" @click.stop.prevent="dialog = true">Terms of Service</a>
                                &nbsp;and&nbsp;
                                <a href="#" @click.stop.prevent="dialog = true">Privacy Policy</a>*
                            </template>
                        </v-checkbox>
                    </v-form>
                    <v-divider></v-divider>

                    <v-dialog v-model="dialog" max-width="400" persistent>
                        <v-card>
                            <v-card-title class="text-h5 bg-grey-lighten-3"> Legal </v-card-title>
                            <v-card-text>
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
                                minim veniam, quis nostrud exercitation ullamco laboris nisi ut
                                aliquip ex ea commodo consequat. Duis aute irure dolor in
                                reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
                                pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
                                culpa qui officia deserunt mollit anim id est laborum.
                            </v-card-text>
                            <v-divider></v-divider>
                            <v-card-actions>
                                <v-btn variant="text" @click="agreement = false, dialog = false">
                                    No
                                </v-btn>
                                <v-spacer></v-spacer>
                                <v-btn color="deep-purple" variant="tonal" @click="agreement = true, dialog = false">
                                    Yes
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-card>
                <v-card-actions>
                    <v-btn color="primary" @click="prevStep" :disabled="currentStep === 1">
                        上一步
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click="nextStep" :disabled="!isValid">
                        下一步
                    </v-btn>
                </v-card-actions>
            </template>
            <template v-slot:item.3>
                <v-card-title>新增老婆</v-card-title>
                <v-card-text>醒醒，你沒有老婆</v-card-text>
                <v-card-actions>
                    <v-btn color="primary" @click="prevStep" :disabled="currentStep === 1">
                        上一步
                    </v-btn>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click="completeProcess" :disabled="false">
                        完成
                    </v-btn>
                </v-card-actions>
            </template>
        </v-stepper>
    </v-container>
</template>

<script lang="ts" setup>
    import { useAppStore } from '@/stores/app';
    import { useRouter } from 'vue-router'

    const store = useAppStore()
    const router = useRouter()

    const steps = ['新增老婆', '步驟二', '步驟三']
    const currentStep = ref(1)
    const selectedCard = ref(0); // 儲存選擇的卡片索引
    const wives = [
        { name: '老婆1', text: 'test1' },
        { name: '老婆2', text: 'test2' },
        { name: '老婆3', text: 'test3' },
        { name: '老婆4', text: 'test4' },
        { name: '老婆5', text: 'test5' },
        { name: '老婆6', text: 'test6' },
    ];

    const isValid = ref(false)
    const character = ref('')
    const backStory = ref('')
    const agreement = ref(false)
    const dialog = ref(false)


    // 點擊卡片時更新選擇的卡片索引
    const selectCard = (index: number) => {
        selectedCard.value = index;
    };
    const rules = {
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
    const completeProcess = () => {
        router.push('/app')
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