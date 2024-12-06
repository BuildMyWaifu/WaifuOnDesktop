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
                        <v-col cols="12" md="4" v-for="(wife, index) in wives" :key="index">
                            <v-card variant="plain" @click="selectCard(index)"
                                :class="{ 'selected-card': selectedCard === index }">
                                <v-card-title>{{ wife.profile.name }}</v-card-title>
                                <v-card-text>{{ wife.profile.description }}</v-card-text>
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
                    <CompanionEdit v-model="companion"></CompanionEdit>
                    <v-divider></v-divider>
                    <v-card-actions>
                        <v-btn color="primary" @click="prevStep" :disabled="currentStep === 1">
                            上一步
                        </v-btn>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="CloseDialog">
                            完成
                        </v-btn>
                    </v-card-actions>
                </template>
            </v-stepper>
        </v-container>
    </v-dialog>
</template>

<script lang="ts" setup>
    import CompanionEdit from './CompanionEdit.vue';
    import { Companion } from '@/utils/model';

    const isDialogOpen = ref(false)
    const steps = ['選擇老婆', '設定']
    const currentStep = ref(1)
    const selectedCard = ref() // 儲存選擇的卡片索引
    const companion = ref<Companion>({
        _id: '',
        userId: '',
        profile: {
            name: '',
            description: '',
        },
        prompt: {
            character: '',
            backstory: '',
        },
    });

    const wives = [
    {
        _id: "咪醬",
        userId: '',
        profile: {
        name: "咪醬",
        description: "可愛又元氣滿滿的貓娘女僕，喜歡撒嬌和主人喵～！",
        },
        prompt: {
        character: "元氣可愛的貓娘女僕",
        backstory:
            "咪醬天生就是一隻充滿愛與熱情的貓娘，最喜歡主人，讓主人的每一天都充滿幸福和快樂喵！",
        },
    },
    {
        _id: '牛肉薩滿',
        userId: '',
        profile: {
            name: '牛肉薩滿',
            description: 'Heart<33333',
        },
        prompt: {
            character: '腹黑的AI女鵝',
            backstory: '牛肉本來只是打個OSU，不知不覺便成了爆紅AI實況主',
        },
    },
    {
        _id: '愛麗絲',
        userId: '',
        profile: {
            name: '愛麗絲',
            description: '歡迎老師，愛麗絲在等著老師',
        },
        prompt: {
            character: '女僕勇者',
            backstory: '在廢墟發現的來歷不明的少女。包含年齡在內，所有情報都無法推斷。現在跟著綠和桃井玩遊戲，已經變成重度遊戲狂熱者了。',
        },
    },
    {
        _id: '彌香',
        userId: '',
        profile: {
            name: '彌香',
            description: '阿哈哈~牡蠣牡蠣~',
        },
        prompt: {
            character: '三一綜合學園的學生',
            backstory: '三一綜合學園所屬，是擔任構成三一的學生聯盟「聖父派」前任領袖的少女。原本是茶會的一員，和主席渚是青梅竹馬。然而由於政治上屬於對立立場，她秉持著公私分明的態度。雖然她總是露出開心的笑容，展現天真無邪的樣子，但心裡似乎有著無法與他人訴說的煩惱。',
        },
    },
    {
        _id: '陽奈',
        userId: '',
        profile: {
            name: '陽奈',
            description: '雖然很麻煩，不過必須做該做的事，因為那就是我的義務',
        },
        prompt: {
            character: '格黑娜學園的糾察部長',
            backstory: '平常是覺得什麼都很麻煩的懶蟲少女，但是一旦在和校規有關的問題上，就會展現出嚴格的糾察部长的樣子。經常把「好麻煩」作為口頭禪，但在戰場上從不迷茫，快速判斷並行動。因此與格黑娜敵對的組織最害怕她出場戰鬥',
        },
    },
        {
        _id: '',
        userId: '',
        profile: {
            name: '自定義',
            description: '',
        },
        prompt: {
            character: '',
            backstory: '',
        },
    }
    ];

    // 點擊卡片時更新選擇的卡片索引
    const selectCard = (index: number) => {
        selectedCard.value = index;
        companion.value = { ...wives[index] };
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