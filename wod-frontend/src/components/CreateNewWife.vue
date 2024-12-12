<!-- eslint-disable vue/valid-v-slot -->
<template>
    <v-dialog v-model="isDialogOpen" @update:model-value="() => {
        currentStep = 1
    }" scrollable fullscreen>
        <template v-slot:activator="{ props }">
            <v-btn v-bind="props" variant="flat">
                <template v-slot:prepend>
                    <v-icon icon="mdi-plus"></v-icon>
                </template>
                新增老婆
            </v-btn>
        </template>
        <v-container class="d-flex align-center h-100">
            <v-stepper v-model="currentStep" :items="steps" prev-text="上一步" :next-text="currentStep == 2 ? '完成' : '下一步'"
                >
                <template v-slot:item.1>
                    <div>
                        <v-card-subtitle>從範本建立，或是從零開始打造</v-card-subtitle>
                        <div class="d-flex" style="max-height: 60vh;">
                            <v-list lines="three" style="max-height: 100%;min-width: 256px;" class="overflow-y-auto">
                                <v-list-item v-for="companion, i in wives" :key="i" :title="companion.profile.name"
                                    :subtitle="companion.profile.description" @click="selectBase(i)"
                                    :active="baseCompanionIndex == i">
                                </v-list-item>
                            </v-list>
                            <v-divider vertical></v-divider>
                            <CompanionPreview readonly :companion="wives[baseCompanionIndex]" class="overflow-y-auto">
                            </CompanionPreview>
                        </div>
                    </div>
                </template>
                <template v-slot:item.2>
                    <CompanionEdit v-if="companion != undefined" v-model="companion"></CompanionEdit>
                    <v-card-text v-else>
                        不合法的選擇，請回上一步
                        <div class="text-caption text-grey">如果見到此訊息，請視作錯誤回報</div>
                    </v-card-text>
                </template>
            </v-stepper>
        </v-container>
    </v-dialog>
</template>

<script lang="ts" setup>
    import CompanionEdit from './CompanionEdit.vue';
    import CompanionPreview from '@/components/CompanionPreview.vue'
    import { Companion } from '@/utils/model';
    import { copy } from '@/utils/utils'
    import { ref } from 'vue';

    const isDialogOpen = ref(false)
    const steps = ['選擇老婆', '設定']
    const currentStep = ref(1)
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
    ] as Companion[];

    const baseCompanionIndex = ref(0)
    function selectBase(index: number) {
        baseCompanionIndex.value = index
        baseCompanion.value = wives[index]
        companion.value = copy(baseCompanion.value)
    }

    const baseCompanion = ref<Companion>(wives[0])

    const companion = ref<Companion>(wives[0]);


</script>
