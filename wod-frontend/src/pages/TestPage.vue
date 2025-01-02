<template>
    <v-container>
        <v-card-title>測試用頁面</v-card-title>
        <v-btn variant="text" to="/">返回首頁</v-btn>
        <v-btn variant="text" v-if="store.companionList && store.companionList.length != 0"
            :to="`/liveChat/${store.companionList[0]._id}`">liveChat</v-btn>
        <v-btn variant="text" @click="openNewWindow">開啟新視窗</v-btn>
        <v-btn variant="text" @click="updateSyncAndBroadcast">toggle test facetime window</v-btn>
        <!-- <v-btn variant="text" @click="store.generateMockCompanionList">generateMockCompanionList</v-btn> -->
        <v-card-text>
            <pre><code>{{ store.sync }}</code></pre>
        </v-card-text>
        {{ companion }}
        <Live2dComponent
            fromUrl="/api/assets/live2dModel/ca883996-873a-4957-83ee-d752f653d6fb/x79MX9z4C9Q/miku_model/runtime/miku_sample_t04.model3.json">
        </Live2dComponent>
        <CompanionEdit v-if="companion" v-model="companion" />
    </v-container>
</template>
<script lang="ts" setup>
    import Live2dComponent from "@/components/Live2dComponent.vue";
    import { useAppStore } from '@/stores/app'; 
    import { broadcast, createWindow } from '@/utils/electronAPI'
    import CompanionEdit from '@/components/CompanionEdit.vue'
    import { ref, onMounted } from 'vue'
    import { Companion } from '@/utils/model';

    const store = useAppStore()

    function openNewWindow() {
        createWindow('/test')
    }
    const companion = ref<Companion>()
    onMounted(async () => {
        await store.login({ _id: 'test', profile: { avatarId: 'test avatarId', name: 'test name', email: 'test' } })

        // store.generateMockCompanionList()
        if (store.companionList) { 
            companion.value = store.companionList[0]
        }
    })

    function updateSyncAndBroadcast() {

        store.setSync({
            companion: {
                test: {
                    window: {
                        facetime: !store.sync.companion.test?.window.facetime
                    }
                }
            }
        })
        broadcast(store.sync)
    }

</script>