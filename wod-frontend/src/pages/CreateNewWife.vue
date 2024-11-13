<!-- <v-stepper-actions> 尚未處理-->
<template>
    <v-container>
        <v-stepper :items="['Step 1', 'Step 2', 'Step 3']">
            <template v-slot:item.1>
                <v-card-title>新增老婆</v-card-title>
                <v-card-text>111</v-card-text>
            </template>

            <template v-slot:item.2>
                <v-card title="Step Two" flat>...</v-card>
            </template>

            <template v-slot:item.3>
                <v-card title="Step Three" flat>...</v-card>
            </template>
        </v-stepper>
    </v-container>
</template>

<script lang="ts" setup>
    import { useAppStore } from '@/stores/app';
    import { broadcast, createWindow } from '@/utils/electronAPI'

    const store = useAppStore()



</script>