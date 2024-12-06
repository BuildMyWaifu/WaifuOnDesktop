<template>
    <v-container>
        <v-card-title>測試用頁面</v-card-title>
        <v-btn variant="text" to="/">返回首頁</v-btn>
        <v-btn variant="text" to="/liveChat">liveChat</v-btn>
        <v-btn variant="text" @click="openNewWindow">開啟新視窗</v-btn>
        <v-btn variant="text" @click="updateSyncAndBroadcast">toggle test facetime window</v-btn>
        <v-card-text>
            <pre><code>{{ store.sync }}</code></pre>
        </v-card-text>
        {{ companion }}
        <CompanionEdit v-if="companion" v-model="companion" />
    </v-container>
</template>
<script lang="ts" setup>
    import { useAppStore } from '@/stores/app';
    import { broadcast, createWindow } from '@/utils/electronAPI'
    import CompanionEdit from '@/components/CompanionEdit.vue'
    import { ref, onMounted } from 'vue'
    import { Companion } from '@/utils/models';

    const store = useAppStore()

    function openNewWindow() {
        createWindow('/test')
    }
    const companion = ref<Companion>()
    onMounted(async () => {
        await store.login({ _id: 'test', profile: { avatarId: 'test avatarId', name: 'test name', email: 'test' } })

        store.generateMockCompanionList()
        companion.value = store.companionList[0]
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