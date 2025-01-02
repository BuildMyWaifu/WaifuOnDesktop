<!-- eslint-disable vue/valid-v-slot -->
<template>

    <div style="height: 100vh;width: 100vw">
        <v-window v-model="currentStep">
            <v-window-item value="select">
                <div class="d-flex" v-if="currentStep == 'select'">
                    <v-list lines="three" style="min-width: 256px;max-width: 256px; height: 100vh; max-height: 100vh;"
                        class="overflow-y-auto">
                        <v-btn to="/app" prepend-icon="mdi-menu" flat>返回</v-btn>
                        <v-card-title>伴侶建立頁面</v-card-title>
                        <v-card-subtitle>從模板建立，或是從零開始打造</v-card-subtitle>
                        <v-list-item v-for="companion, i in wives" :key="i" :title="companion.name"
                            :subtitle="companion.description" @click="selectBase(i)" :active="baseCompanionIndex == i">
                        </v-list-item>
                    </v-list>
                    <v-divider vertical></v-divider>
                    <div class="d-flex flex-column overflow-y-auto flex-grow-1 pa-4 pr-8"
                        style="height: 100vh; max-height: 100vh;">
                        <v-card class="flex-grow-1 d-flex flex-column" variant="outlined">
                            <div class="d-flex align-center">
                                <v-card-title>以此模板為基準</v-card-title>
                                <v-btn variant="tonal" color="primary" @click="currentStep = 'edit'">使用此模板</v-btn>
                            </div>
                            <CompanionPreview readonly :companion="wives[baseCompanionIndex]" class="flex-grow-1 ml-4"
                                style="max-height: calc(100vh - 98px)" :key="baseCompanionIndex" v-if="showPreview">
                            </CompanionPreview>
                        </v-card>
                    </div>
                </div>

            </v-window-item>
            <v-window-item value="edit">
                <v-card v-if="currentStep == 'edit'" :key="baseCompanionIndex" class="d-flex flex-column"
                    style="height: 100vh;width: 100vw">
                    <div>
                        <v-btn @click="currentStep = 'select'" flat prepend-icon="mdi-keyboard-return">選擇其他模板</v-btn>
                    </div>
                    <div style="padding-left: 100px;padding-right: 100px;">
                        <v-btn size="large" color="success" block variant="tonal" :disabled="!isCompanionValid(companion)" @click="createCompanoin">建立</v-btn>
                    </div>
                    <div class="flex-grow-1 overflow-auto">

                        <CompanionEdit v-if="companion != undefined" v-model="companion" flat>
                        </CompanionEdit>
                        <v-card-text v-else>
                            不合法的選擇，請回上一步
                            <div class="text-caption text-grey">如果見到此訊息，請視作錯誤回報</div>
                        </v-card-text>
                    </div>

                </v-card>
            </v-window-item>
        </v-window>
    </div>
</template>

<script lang="ts" setup>
    import CompanionEdit from '@/components/CompanionEdit.vue';
    import CompanionPreview from '@/components/CompanionPreview.vue'

    import { ref, watch, nextTick } from 'vue';
    import { Companion } from '@/utils/model';
    import { copy, isCompanionValid } from '@/utils/utils'
    import { useRouter } from 'vue-router';
import { postApi } from '@/utils/api';

    
    const currentStep = ref<string>('select')
    const wives = [
        {
            _id: "hiyori",
            userId: '',
            name: "日和",
            description: "溫柔內向的高中少女，用畫筆繪製屬於自己的夢想世界。",
            live2dModelSettingPath: "/api/assets/live2dModel/public/hiyori_pro_use/runtime/hiyori_pro_t11.model3.json",
            poseMap: {
                "angry": {
                    "motion": "motion/angry.motion3.json",
                    "expression": "expressions/idle.exp3.json"
                },
                "attract": {
                    "motion": "motion/attract.motion3.json",
                    "expression": "expressions/idle.exp3.json"
                },
                "curious": {
                    "motion": "motion/curious.motion3.json",
                    "expression": "expressions/idle.exp3.json"
                },
                "excited": {
                    "motion": "motion/excited.motion3.json",
                    "expression": "expressions/idle.exp3.json"
                },
                "relax": {
                    "motion": "motion/relax.motion3.json",
                    "expression": "expressions/idle.exp3.json"
                },
                "sad": {
                    "motion": "motion/sad.motion3.json",
                    "expression": "expressions/idle.exp3.json"
                },
                "shock": {
                    "motion": "motion/shock.motion3.json",
                    "expression": "expressions/idle.exp3.json"
                },
                "shy": {
                    "motion": "motion/shy.motion3.json",
                    "expression": "expressions/idle.exp3.json"
                },
                "smile": {
                    "motion": "motion/smile.motion3.json",
                    "expression": "expressions/idle.exp3.json"
                }
            }
,
            backstory: "日和是一位普通的高中女生，住在城市郊外的一棟老房子裡。她的家中經營著一家小型樂器店，父母希望她繼承家業，但她卻對音樂以外的領域充滿興趣。小時候的日和常常坐在店裡的角落，一邊聽著吉他彈奏的旋律，一邊用手中的畫本勾勒出自己的小世界。\n雖然她對藝術和設計抱有濃厚的興趣，但由於性格內向，總是難以表達自己的想法。直到一次校內的藝術比賽，她因偶然被朋友鼓勵，決定提交自己的作品，最終意外贏得了大獎。這次經歷讓日和找回了自信，也激勵她逐步邁出自己的舒適圈。\n日和非常珍惜與家人和朋友的每一份情感。在日常生活中，她最喜歡的事情是和朋友一起討論夢想，分享創意靈感。她的目標是創作出能夠打動人心的作品，將溫暖與幸福帶給更多的人。",
            // TODO: generate trait
        },
        {
            _id: "natori",
            userId: '',
            name: "名執",
            description: "冷靜優雅的完美執事，忠於職責並時刻守護身邊的人。",
            live2dModelSettingPath: "/api/assets/live2dModel/public/natori_pro_use/runtime/natori_pro_t06.model3.json",
            poseMap: {
                "angry": {
                    "motion": "motions/react_big.motion3.json",
                    "expression": "exp/angry.exp3.json"
                },
                "attract": {
                    "motion": "motions/push_glasses.motion3.json",
                    "expression": "exp/attract.exp3.json"
                },
                "blush": {
                    "motion": "motions/react_small.motion3.json",
                    "expression": "exp/blush.exp3.json"
                },
                "confident": {
                    "motion": "motions/bow.motion3.json",
                    "expression": "exp/confident.exp3.json"
                },
                "confuse": {
                    "motion": "motions/curious.motion3.json",
                    "expression": "exp/confuse.exp3.json"
                },
                "idle": {
                    "motion": "motions/idle.motion3.json",
                    "expression": "exp/idle.exp3.json"
                },
                "mischievous": {
                    "motion": "motions/react_small.motion3.json",
                    "expression": "exp/mischievous.exp3.json"
                },
                "sad": {
                    "motion": "motions/look_away.motion3.json",
                    "expression": "exp/sad.exp3.json"
                },
                "shock": {
                    "motion": "motions/react_big.motion3.json",
                    "expression": "exp/shock.exp3.json"
                },
                "smile": {
                    "motion": "motions/react_small.motion3.json",
                    "expression": "exp/smile.exp3.json"
                }
            }
,
            backstory: "名執出生于一個傳統的執事家族，從小便被嚴格訓練以繼承家族的使命。他的父親是貴族世家最為信任的管家，而名執則在耳濡目染中學習了禮儀、管理與戰鬥技能。他天資聰穎，很快便超越了同齡人，成為一位全能型的執事。儘管名執表面一絲不苟，但他並非冰冷無情之人。在完成日常工作的間隙，他會偷偷翻閱經典文學，特別是那些講述騎士與忠誠的書籍。他始終堅信，執事的職責不僅是照料主人，更是成為主人的堅實後盾，在需要時毫不猶豫地站到最前線保護她。他現在效力於一位年輕的大小姐，除了日常事務，他還承擔了保護她安全的職責。由於大小姐性格調皮，名執經常需要化解她製造的各種麻煩，但他從未因此抱怨，反而認為這是與主人之間的羈絆逐漸加深的方式。",
            // TODO: generate trait
        },
        {
            _id: "mao",
            userId: '',
            name: "麻央",
            description: "充滿童心與創造力的自由畫家，用畫筆為世界增添色彩。",
            live2dModelSettingPath: "/api/assets/live2dModel/public/mao_test/mao_pro_test.model3.json",
            poseMap: {
                "happy_smile": {
                    "motion": "motions/wink.motion3.json",
                    "expression": "expressions/smile.exp3.json"
                },
                "nervous_smile": {
                    "motion": "motions/look_away.motion3.json",
                    "expression": "expressions/blush.exp3.json"
                },
                "shy": {
                    "motion": "motions/relax.motion3.json",
                    "expression": "expressions/blush.exp3.json"
                },
                "sad": {
                    "motion": "motions/heart_fail.motion3.json",
                    "expression": "expressions/sad.exp3.json"
                },
                "surprised": {
                    "motion": "motions/react_big.motion3.json",
                    "expression": "expressions/shock.exp3.json"
                },
                "angry": {
                    "motion": "motions/react_big.motion3.json",
                    "expression": "expressions/angry.exp3.json"
                },
                "confident": {
                    "motion": "motions/level_up.motion3.json",
                    "expression": "expressions/confident.exp3.json"
                },
                "mischievous": {
                    "motion": "motions/react_small.motion3.json",
                    "expression": "expressions/mischievous.exp3.json"
                },
                "confused": {
                    "motion": "motions/look_away.motion3.json",
                    "expression": "expressions/confuse.exp3.json"
                },
                "idle": {
                    "motion": "motions/relax.motion3.json",
                    "expression": "expressions/idle.exp3.json"
                },
                "attracted": {
                    "motion": "motions/heart_success.motion3.json",
                    "expression": "expressions/attract.exp3.json"
                }
            },
            backstory: "麻央是一位年輕的自由畫家，以她大膽的色彩運用和奇思妙想而聞名。她相信畫筆是她表達內心世界的鑰匙，而畫布則是她創造夢想的舞臺。麻央的畫風獨特，常常將現實與幻想融合在一起，構建出充滿活力與魔幻氣息的世界。她從小便對繪畫充滿熱情，無論是牆壁、地板還是自己的衣服，都是她的“畫布”。家人雖然經常無奈於她的“塗鴉”，但也逐漸被她的熱情和天賦所折服。如今，麻央的作品已經成為許多展覽中的焦點，她用畫筆勾勒出的不僅是畫作，更是一種充滿想像力的生活態度。麻央始終相信，每個人的生活都應該被鮮豔的色彩裝點，她的目標是通過自己的作品，帶給世界更多的快樂與希望。",
            // TODO: generate trait
        },
      
        {
            _id: '',
            userId: '',
            name: '自定義',
            description: '自定義',
            live2dModelSettingPath: '',
            poseMap: {},
            backstory: '',
        }
    ] as Companion[];


    const baseCompanionIndex = ref(0)
    function selectBase(index: number) {
        baseCompanionIndex.value = index
        baseCompanion.value = wives[index]
        companion.value = copy(baseCompanion.value)
    }
    const showPreview = ref(false)
    function reloadPreview() {
        showPreview.value = false
        nextTick(() => { showPreview.value = true })
    }
    watch(currentStep, reloadPreview)
    reloadPreview()

    const baseCompanion = ref<Companion>(wives[0])

    const companion = ref<Companion>(wives[0]);

    const router = useRouter()

    async function createCompanoin() {
        const res = await postApi(`/api/companion`, {
            name: companion.value.name,
            description: companion.value.description,
            live2dModelSettingPath: companion.value.live2dModelSettingPath,
            poseMap: companion.value.poseMap,
            backstory: companion.value.backstory
        })
        if (res.status == 'success') {
            router.push("/app/" + res.data._id)
        } else {
            alert(res.message)
        }

    }
</script>
