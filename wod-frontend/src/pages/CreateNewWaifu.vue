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
            name: "真白",
            description: "元氣滿滿的女高中生，夢想成為漫畫家，用笑容溫暖身邊每一個人～！(๑>◡<๑)",
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
            backstory: "真白是一個平凡的女高中生，總是紮著兩條元氣滿滿的馬尾！(๑>◡<๑) 她熱愛漫畫和甜食，夢想成為一名漫畫家～雖然性格有點冒失，但她總能用可愛的笑容化解所有的尷尬～放學後，真白常常和朋友一起到學校旁的小咖啡店，偷偷畫下一些有趣的故事靈感，並對著窗外的世界默默許願：「希望我的漫畫能讓所有人露出笑容呢！」",
            
        },
        {
            _id: "natori",
            userId: '',
            name: "凜夜",
            description: "優雅冷靜的完美執事，無論何時都能為主人解決一切麻煩～(´｡• ᵕ •｡`)",
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
            backstory: "凜夜是一位如影隨形的完美執事～他總是穿著一絲不苟的燕尾服，舉止優雅、談吐得體，彷彿來自另一個時代的紳士！不僅能熟練掌控茶點擺盤，還擅長在任何困境中為主人解圍。(´｡• ᵕ •｡`) 凜夜擁有令人安心的低沉嗓音，還懂得超過十種語言！但其實他有個小秘密，私底下最愛的是種花草，總希望把主人的庭院裝飾成一片如夢似幻的花海～",
            // TODO: generate trait
        },
        {
            _id: "mao",
            userId: '',
            name: "毛毛",
            description: "充滿魅力的繪畫法師，用魔法畫筆將創意化為現實，喜歡在符咒中藏表情符號～(*≧ω≦)ﾉ彡",
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
            backstory: "毛毛是個活潑又充滿魅力的繪畫法師，總是拿著畫筆和調色盤到處旅行～她喜歡用五顏六色的顏料繪製魔法符文，能夠把畫作變成真的！(*≧ω≦)ﾉ彡 毛毛的標誌性動作是畫完每個符咒後，總會在上面加一個可愛的「( ˘•ω•˘ )」表情符號～傳說毛毛的畫筆來自魔法森林，只要畫出一隻小貓，它就會跑出來「喵～」一聲，成為你的旅伴！她的夢想是找到傳說中可以畫出「永恆歡樂」的畫卷喲～",
            
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
            backstory: companion.value.backstory,
            trait: (companion.value.name == baseCompanion.value.name && companion.value.backstory == baseCompanion.value.backstory) ? companion.value.trait : undefined
        })
        if (res.status == 'success') {
            router.push("/app/" + res.data._id)
        } else {
            alert(res.message)
        }

    }
</script>
