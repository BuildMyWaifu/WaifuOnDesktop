<template>
    <v-container>
        <v-card-title>測試用頁面</v-card-title>
        <v-btn variant="text" to="/">返回首頁</v-btn>
        <v-btn variant="text" @click="openNewWindow">開啟新視窗</v-btn>
        <v-btn variant="text" @click="updateSyncAndBroadcast">toggle test facetime window</v-btn>
        <v-card-text>
            <pre><code>{{store.sync}}</code></pre>
        </v-card-text>
    </v-container>
</template>
<script lang="ts" setup>
import { useAppStore } from '@/stores/app';
    import { broadcast, createWindow } from '@/utils/electronAPI'

const store = useAppStore()

function openNewWindow(){
    createWindow('/test')
}

function updateSyncAndBroadcast(){

    store.setSync({
        companion: {
            test: {
                window: {
                    facetime: ! store.sync.companion.test?.window.facetime
                }
            }
        }
    })
    broadcast(store.sync)
}

</script>